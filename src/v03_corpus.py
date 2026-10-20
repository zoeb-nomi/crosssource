"""Build the frozen v0.3 corpus from cached CourtListener responses.

Reads   data/raw/opinions/<opinion_id>.json       (REST v4 opinion response, verbatim; src/v03_fetch.py)
        data/raw/opinions/<opinion_id>.meta.json  (provenance written by src/v03_fetch.py)
Writes  data/v0.3/corpus/cl<opinion_id>.txt       (normalised opinion text)
        data/v0.3/sources.json                    (per-document provenance)

Normalisation (LABELING_PROTOCOL.md §2.2) is deterministic and frozen once
items reference chunk ids: HTML tags stripped, entities unescaped, PDF page
headers / page numbers dropped, hard-wrapped lines re-joined into paragraphs.

Usage:  python src/v03_corpus.py
"""

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from retrieval import chunk_text  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "opinions"
OUT = ROOT / "data" / "v0.3"

PAGE_HEADER_RE = re.compile(r"^\s*(USCA\d+ Appeal:|Appellate Case:|Case:\s*\d|USCA Case #).*$", re.I)
PAGE_NUMBER_RE = re.compile(r"^\s*-?\s*\d{1,3}\s*-?\s*$")
# running headers such as "2  ESTATE OF NAJERA-AGUIRRE V. CITY OF RIVERSIDE" (either side of the number)
RUNNING_HEADER_RE = re.compile(r"^\s*(\d{1,3}\s+)?[A-Z0-9 .,'&’\-]{3,} V\. [A-Z0-9 .,'&’\-]{3,}?(\s+\d{1,3})?\s*$")
BLOCK_TAG_RE = re.compile(r"</?(p|div|br|h\d|li|blockquote|tr)\b[^>]*>", re.I)
TAG_RE = re.compile(r"<[^>]+>")


def pdf_text(pdf_path) -> str:
    """Deterministic text from a CourtListener storage PDF (pypdf layout mode keeps paragraph indents)."""
    from pypdf import PdfReader
    return "\f".join(page.extract_text(extraction_mode="layout") or "" for page in PdfReader(pdf_path).pages)


def strip_html(raw: str, plain: bool = False) -> tuple[str, bool]:
    """Return (text, is_preformatted). plain_text and <pre> output keep their line layout."""
    preformatted = plain or "<pre" in raw[:2000].lower()
    if not preformatted:
        raw = BLOCK_TAG_RE.sub("\n\n", raw)
    text = html.unescape(TAG_RE.sub("", raw))
    return text.replace("\r", ""), preformatted


def join_preformatted(text: str) -> list[str]:
    """PDF-derived text: drop page furniture, rebuild paragraphs from indentation."""
    lines = []
    for line in text.replace("\f", "\n").split("\n"):
        if (not line.strip() or PAGE_HEADER_RE.match(line) or PAGE_NUMBER_RE.match(line)
                or RUNNING_HEADER_RE.match(line)):
            continue
        lines.append(line.rstrip())
    if not lines:
        return []
    indents = Counter(len(ln) - len(ln.lstrip()) for ln in lines)
    body = indents.most_common(1)[0][0]
    paras, current = [], []
    for ln in lines:
        indent = len(ln) - len(ln.lstrip())
        if current and indent >= body + 4:
            paras.append(current)
            current = []
        current.append(ln.strip())
    if current:
        paras.append(current)
    out = []
    for p in paras:
        joined = " ".join(p)
        joined = re.sub(r"(\w)- (\w)", r"\1-\2", joined)  # keep hyphenated compounds intact
        out.append(re.sub(r"[ \t]+", " ", joined).strip())
    return [p for p in out if p]


def join_html(text: str) -> list[str]:
    paras = re.split(r"\n\s*\n", text)
    return [re.sub(r"\s+", " ", p).strip() for p in paras if p.strip()]


def normalise(raw: str, plain: bool = False) -> str:
    text, pre = strip_html(raw, plain)
    paras = join_preformatted(text) if pre else join_html(text)
    return "\n".join(paras) + "\n"


def main():
    metas = sorted(RAW.glob("*.meta.json"))
    if not metas:
        sys.exit(f"no cached opinions in {RAW}")
    (OUT / "corpus").mkdir(parents=True, exist_ok=True)
    sources = []
    for mpath in metas:
        meta = json.loads(mpath.read_text(encoding="utf-8"))
        oid = meta["opinion_id"]
        field = meta["text_field"]
        if field == "storage_pdf":
            raw_text = pdf_text(ROOT / "data" / "raw" / "pdf" / f"{oid}.pdf")
            text = normalise(raw_text, plain=True)
        else:
            resp = json.loads((RAW / f"{oid}.json").read_text(encoding="utf-8"))
            assert resp.get("id") == oid, f"{oid}: raw response id mismatch"
            raw_text = resp[field]
            text = normalise(raw_text, plain=field == "plain_text")
        doc_id = f"cl{oid}"
        (OUT / "corpus" / f"{doc_id}.txt").write_text(text, encoding="utf-8")
        chunks = chunk_text(text)
        sources.append({
            "doc_id": doc_id,
            **{k: meta.get(k) for k in ("opinion_id", "cluster_id", "case_name", "court_id", "date_filed",
                                         "citation", "docket_number", "url", "opinion_type", "topic_key",
                                         "area_of_law")},
            # CourtListener's own field (Published / Unpublished) — not to be confused with precedential_status below
            "publication_status": meta.get("precedential_status", "Published"),
            "text_field": field, "raw_chars": len(raw_text),
            **({k: meta[k] for k in ("pdf_url", "pdf_sha1")} if field == "storage_pdf" else {}),
            "chars": len(text),
            "words": len(text.split()),
            "chunks": len(chunks),
            "api_url": meta["api_url"],
            "source": ("CourtListener file storage PDF, SHA-1 verified against the REST v4 search response (Free Law Project)"
                       if field == "storage_pdf" else "CourtListener REST API v4 (Free Law Project)"),
        })
        print(f"{doc_id:14} {meta['court_id']:6} {meta['date_filed']}  {len(text.split()):6} words  "
              f"{len(chunks):3} chunks  {meta['case_name'][:50]}")
    # precedential status (good law / abrogated / overruled / unknown) from the treatment screen + review
    treatment_path = OUT / "treatment.json"
    treatment = json.loads(treatment_path.read_text(encoding="utf-8")) if treatment_path.exists() else {}
    for s in sources:
        t = treatment.get(str(s["opinion_id"]), {})
        s["precedential_status"] = t.get("precedential_status", "unknown")
        s["precedential_status_basis"] = t.get("basis", "not screened")
        s["precedential_status_checked"] = t.get("reviewed_at") or t.get("screened_at")
    sources.sort(key=lambda s: s["doc_id"])
    (OUT / "sources.json").write_text(json.dumps(sources, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\n{len(sources)} documents -> {OUT / 'corpus'}")


if __name__ == "__main__":
    main()
