"""CrossSource v0.3 dataset pipeline (after src/v03_corpus.py).

Subcommands
  packets      per-topic generator packets: every chunk of every opinion, by topic
  assemble     drafts (generator output) -> items with provenance + rater A labels
  validate     provenance / balance checks from LABELING_PROTOCOL.md §1.3, §2, §5
  rater-input  label-free rater packets (what rater B is allowed to see)
  agreement    rater A vs rater B -> AGREEMENT data (percent agreement, Cohen's kappa)
  adjudication disagreements + seeded 10% of agreements -> adjudication queue JSON

All paths are under data/v0.3/. Work files live in data/v0.3/work/.

Usage:  python src/v03_dataset.py <subcommand> [--labels-b PATH] [--round N]
"""

import argparse
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from retrieval import chunk_text  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
V3 = ROOT / "data" / "v0.3"
WORK = V3 / "work"
CC_LABELS = ["supported", "right_doc_wrong_passage", "wrong_document", "unsupported_claim"]
TARGET_CC = {"supported": 30, "right_doc_wrong_passage": 15, "wrong_document": 15, "unsupported_claim": 15}
WINDOW = 5
SEED = 20261019
CITATION_RE = re.compile(r"\b\d{1,4} (U\.S\.|S\. ?Ct\.|F\.(2d|3d|4th)?|F\. ?Supp\.( 2d| 3d)?|"
                         r"[A-Z][A-Za-z.]*\.( ?[23]d| ?4th| ?5th)?|N\.[EW]\.( ?[23]d)?|P\.( ?[23]d)?|"
                         r"A\.( ?[23]d)?|S\.[EW]\.( ?[23]d)?|So\.( ?[23]d)?|Cal\.( ?[45]th| ?App\.)?) \d{1,5}")


def jl_read(path):
    return [json.loads(ln) for ln in Path(path).read_text(encoding="utf-8").splitlines() if ln.strip()]


def jl_write(path, rows):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def load_sources():
    return {s["doc_id"]: s for s in json.loads((V3 / "sources.json").read_text(encoding="utf-8"))}


def load_chunks():
    chunks = {}
    for path in sorted((V3 / "corpus").glob("*.txt")):
        for i, text in enumerate(chunk_text(path.read_text(encoding="utf-8"))):
            chunks[f"{path.stem}:{i}"] = text
    return chunks


def doc_of(cid):
    return cid.split(":")[0]


def window_for(gt, n_chunks):
    """≤ WINDOW consecutive chunk indices covering the ground truth, clipped to the document."""
    idx = sorted(int(c.split(":")[1]) for c in gt)
    lo, hi = idx[0], idx[-1]
    while hi - lo + 1 < WINDOW and (lo > 0 or hi < n_chunks - 1):
        if lo > 0:
            lo -= 1
        if hi - lo + 1 < WINDOW and hi < n_chunks - 1:
            hi += 1
    return [f"{doc_of(gt[0])}:{i}" for i in range(lo, hi + 1)]


# --------------------------------------------------------------------------- packets
def cmd_packets(_):
    sources, chunks = load_sources(), load_chunks()
    by_topic = defaultdict(list)
    for doc_id, s in sources.items():
        by_topic[s["topic_key"]].append(doc_id)
    for topic, docs in sorted(by_topic.items()):
        packet = {"topic_key": topic, "documents": []}
        for d in sorted(docs):
            s = sources[d]
            packet["documents"].append({
                "doc_id": d, "case_name": s["case_name"], "court_id": s["court_id"],
                "date_filed": s["date_filed"], "area_of_law": s["area_of_law"],
                "chunks": [{"id": cid, "has_case_citation": bool(CITATION_RE.search(t)), "text": t}
                           for cid, t in chunks.items() if doc_of(cid) == d],
            })
        out = WORK / "packets" / f"{topic}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(packet, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"{topic:24} {len(docs)} docs  {sum(len(x['chunks']) for x in packet['documents'])} chunks")


# --------------------------------------------------------------------------- assemble
def cmd_assemble(_):
    sources, chunks = load_sources(), load_chunks()
    drafts = []
    for path in sorted((WORK / "drafts").glob("*.jsonl")):
        drafts.extend(jl_read(path))
    qa, cc, rater_a, hidden = [], [], [], []
    for d in drafts:
        if d["type"] == "qa_citation":
            gt = d["ground_truth_chunks"]
            doc = doc_of(gt[0])
            n = sum(1 for c in chunks if doc_of(c) == doc)
            item = {
                "id": d["draft_key"], "type": "qa_citation", "topic_key": d["topic_key"],
                "area_of_law": sources[doc]["area_of_law"], "question": d["question"],
                "reference_notes": d["reference_notes"], "ground_truth_chunks": gt,
                "candidate_window": window_for(gt, n),
            }
            label = gt
            passage_ids = gt
            qa.append(item)
        else:
            doc = doc_of(d["cited_chunk"])
            ctx = list(d["context_chunks"])
            random.Random(f"{SEED}:{d['claim']}").shuffle(ctx)
            item = {
                "id": d["draft_key"], "type": "citation_check", "topic_key": d["topic_key"],
                "area_of_law": sources[doc]["area_of_law"], "claim": d["claim"],
                "cited_chunk": d["cited_chunk"], "context_chunks": ctx, "label": d["label"],
            }
            label = d["label"]
            passage_ids = [d["cited_chunk"]]
            cc.append(item)
        s = sources[doc]
        item["provenance"] = {
            "doc_id": doc, "opinion_id": s["opinion_id"], "cluster_id": s["cluster_id"], "url": s["url"],
            "case_name": s["case_name"], "court_id": s["court_id"], "date_filed": s["date_filed"],
            "passage": "\n".join(chunks[c] for c in passage_ids),
            "cited_authority": d["cited_authority"],
        }
        rater_a.append({"id": item["id"], "label": label, "reason": d.get("rater_a_reason", "")})
        hidden.append({"id": item["id"], "draft_key": d.get("draft_key"), "construction_note": d.get("construction_note", "")})
    jl_write(V3 / "qa_citation.jsonl", qa)
    jl_write(V3 / "citation_check.jsonl", cc)
    jl_write(V3 / "labels" / "rater_a.jsonl", rater_a)
    jl_write(WORK / "construction_notes.jsonl", hidden)
    print(f"assembled {len(qa)} qa_citation + {len(cc)} citation_check")


# --------------------------------------------------------------------------- validate
def cmd_validate(args):
    sources, chunks = load_sources(), load_chunks()
    corpus_text = {p.stem: p.read_text(encoding="utf-8") for p in (V3 / "corpus").glob("*.txt")}
    qa, cc = jl_read(V3 / "qa_citation.jsonl"), jl_read(V3 / "citation_check.jsonl")
    problems = []
    for it in qa + cc:
        p = it["provenance"]
        for k in ("opinion_id", "cluster_id", "url", "case_name", "court_id", "date_filed", "passage", "cited_authority"):
            if not p.get(k):
                problems.append(f"{it['id']}: empty provenance.{k}")
        if p["date_filed"] < "2018-01-01":
            problems.append(f"{it['id']}: date_filed {p['date_filed']} < 2018")
        for part in p["passage"].split("\n"):
            if part and part not in corpus_text[p["doc_id"]]:
                problems.append(f"{it['id']}: passage not an exact substring of corpus/{p['doc_id']}.txt")
                break
        if p.get("cited_authority") and p["cited_authority"] not in p["passage"]:
            problems.append(f"{it['id']}: cited_authority not verbatim in passage: {p['cited_authority']!r}")
        ids = it.get("candidate_window", []) + it.get("context_chunks", []) + it.get("ground_truth_chunks", [])
        for cid in ids:
            if cid not in chunks:
                problems.append(f"{it['id']}: unknown chunk {cid}")
    for it in qa:
        if not set(it["ground_truth_chunks"]) <= set(it["candidate_window"]):
            problems.append(f"{it['id']}: ground truth outside window")
    for it in cc:
        ctx = it["context_chunks"]
        same = [c for c in ctx if doc_of(c) == doc_of(it["cited_chunk"]) and c != it["cited_chunk"]]
        other = [c for c in ctx if doc_of(c) != doc_of(it["cited_chunk"])]
        if it["cited_chunk"] not in ctx or not same or not other or len(ctx) != 5:
            problems.append(f"{it['id']}: context set must be 5 incl. cited, ≥1 same-doc, ≥1 other-doc")
        if it["label"] not in CC_LABELS:
            problems.append(f"{it['id']}: bad label {it['label']}")

    items = qa + cc
    per_doc = Counter(it["provenance"]["doc_id"] for it in items)
    per_court = Counter(it["provenance"]["court_id"] for it in items)
    fed = sum(1 for it in items if re.fullmatch(r"ca\d+|cadc|cafc", it["provenance"]["court_id"]))
    areas = Counter(it["area_of_law"] for it in items)
    n = len(items)
    report = {
        "items": n, "qa_citation": len(qa), "citation_check": len(cc),
        "cc_label_mix": dict(Counter(it["label"] for it in cc)),
        "qa_gt_sizes": dict(Counter(len(it["ground_truth_chunks"]) for it in qa)),
        "distinct_opinions": len(per_doc), "max_items_per_opinion": max(per_doc.values()) if per_doc else 0,
        "federal_share": round(fed / n, 3) if n else 0, "max_court_share": round(max(per_court.values()) / n, 3) if n else 0,
        "area_of_law": dict(areas), "max_area_share": round(max(areas.values()) / n, 3) if n else 0,
        "problems": problems,
    }
    # precedential status of every opinion an item touches (source, window, context) — LABELING_PROTOCOL §2
    status_notes = []
    status = {d: s.get("precedential_status", "not_checked") for d, s in sources.items()}
    for it in items:
        docs = {doc_of(c) for c in it.get("candidate_window", []) + it.get("context_chunks", [])} | {it["provenance"]["doc_id"]}
        for d in sorted(docs):
            if status.get(d) in ("abrogated", "overruled"):
                status_notes.append(f"{it['id']}: uses {d} (precedential_status={status[d]})")
    # recorded, not a selection criterion (protocol v1.1 §2) — reported loudly, never silently
    report["precedential_status"] = dict(Counter(status.values()))
    report["items_touching_abrogated_or_overruled"] = status_notes
    if report["distinct_opinions"] < 40: problems.append("fewer than 40 distinct opinions")
    if report["max_items_per_opinion"] > 4: problems.append("an opinion supplies more than 4 items")
    if not 0.4 <= report["federal_share"] <= 0.6: problems.append("federal share outside 40–60%")
    if report["max_court_share"] > 0.15: problems.append("a court supplies more than 15% of items")
    if report["max_area_share"] > 0.30: problems.append("an area_of_law tag above 30%")
    (V3 / "validation.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "problems"}, indent=2))
    print(f"precedential_status: {report['precedential_status']}; items touching an abrogated/overruled opinion: {len(status_notes)}")
    for n in status_notes[:20]:
        print("  ! ", n)
    print(f"{len(problems)} problems")
    for p in problems[:60]:
        print("  -", p)
    return problems


# --------------------------------------------------------------------------- rater input
def cmd_import_labels(args):
    """Translate a rater's opaque-id output back to item ids -> labels/rater_b_round<N>.jsonl."""
    id_map = json.loads((WORK / "rater_id_map.json").read_text())
    rows = jl_read(args.src)
    out = []
    for r in rows:
        out.append({**r, "id": id_map[r["id"]]})
    dest = V3 / "labels" / f"rater_b_round{args.round}.jsonl"
    existing = {r["id"]: r for r in jl_read(dest)} if dest.exists() and args.append else {}
    existing.update({r["id"]: r for r in out})
    jl_write(dest, sorted(existing.values(), key=lambda r: r["id"]))
    print(f"imported {len(out)} labels -> {dest} ({len(existing)} total)")


def cmd_rater_input(args):
    chunks = load_chunks()
    rows = []
    for it in jl_read(V3 / "qa_citation.jsonl"):
        rows.append({"id": it["id"], "type": "qa_citation", "question": it["question"],
                     "reference_notes": it["reference_notes"],
                     "candidate_window": [{"id": c, "text": chunks[c]} for c in it["candidate_window"]]})
    for it in jl_read(V3 / "citation_check.jsonl"):
        rows.append({"id": it["id"], "type": "citation_check", "claim": it["claim"],
                     "cited": {"id": it["cited_chunk"], "text": chunks[it["cited_chunk"]]},
                     "others": [{"id": c, "text": chunks[c]} for c in it["context_chunks"] if c != it["cited_chunk"]]})
    # opaque ids: draft keys encode build order (and so, for citation_check, the target label)
    import hashlib
    id_map = {}
    for r in rows:
        opaque = "r" + hashlib.sha256(f"{SEED}:{r['id']}".encode()).hexdigest()[:8]
        id_map[opaque] = r["id"]
        r["id"] = opaque
    (WORK / "rater_id_map.json").write_text(json.dumps(id_map, indent=1) + "\n", encoding="utf-8")
    # batches of 25, items interleaved so a rater never sees one topic in a run
    random.Random(SEED).shuffle(rows)
    out = Path(args.out) if getattr(args, "out", None) else WORK / "rater_input"
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*.jsonl"):
        old.unlink()
    for b in range(0, len(rows), 25):
        jl_write(out / f"batch_{b // 25 + 1:02d}.jsonl", rows[b:b + 25])
    print(f"{len(rows)} label-free items in {(len(rows) + 24) // 25} batches -> {out}")


# --------------------------------------------------------------------------- agreement
def cohen_kappa(a, b):
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def load_labels(path):
    return {r["id"]: r for r in jl_read(path)}


def compare(labels_b_path):
    qa = {it["id"]: it for it in jl_read(V3 / "qa_citation.jsonl")}
    cc = {it["id"]: it for it in jl_read(V3 / "citation_check.jsonl")}
    A, B = load_labels(V3 / "labels" / "rater_a.jsonl"), load_labels(labels_b_path)
    missing = sorted(set(A) - set(B))
    res = {"missing_b": missing}

    ids = sorted(i for i in cc if i in B)
    a = [A[i]["label"] for i in ids]
    b = [B[i]["label"] for i in ids]
    conf = defaultdict(Counter)
    for x, y in zip(a, b):
        conf[x][y] += 1
    res["citation_check"] = {
        "n": len(ids), "percent_agreement": round(sum(x == y for x, y in zip(a, b)) / len(ids), 4) if ids else None,
        "kappa": round(cohen_kappa(a, b), 4) if ids else None,
        "confusion_a_rows_b_cols": {k: dict(v) for k, v in conf.items()},
        "disagreements": [i for i, x, y in zip(ids, a, b) if x != y],
    }

    ids = sorted(i for i in qa if i in B)
    exact, jac, da, db, dis = 0, [], [], [], []
    for i in ids:
        sa, sb = set(A[i]["label"]), set(B[i]["label"] or [])
        exact += sa == sb
        jac.append(len(sa & sb) / len(sa | sb) if sa | sb else 1.0)
        for c in qa[i]["candidate_window"]:
            da.append(c in sa)
            db.append(c in sb)
        if sa != sb:
            dis.append(i)
    res["qa_citation"] = {
        "n": len(ids), "exact_set_agreement": round(exact / len(ids), 4) if ids else None,
        "chunk_decisions": len(da), "chunk_percent_agreement": round(sum(x == y for x, y in zip(da, db)) / len(da), 4) if da else None,
        "chunk_kappa": round(cohen_kappa(da, db), 4) if da else None,
        "mean_jaccard": round(sum(jac) / len(jac), 4) if jac else None,
        "disagreements": dis,
    }
    res["bad_item_flags"] = sorted(i for i, r in B.items() if r.get("bad_item"))
    return res


def cmd_agreement(args):
    res = compare(args.labels_b)
    out = V3 / "labels" / f"agreement_round{args.round}.json"
    out.write_text(json.dumps(res, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "disagreements"} if isinstance(v, dict) else v
                      for k, v in res.items()}, indent=2))
    print(f"disagreements: cc={len(res['citation_check']['disagreements'])} qa={len(res['qa_citation']['disagreements'])} "
          f"bad_item={len(res['bad_item_flags'])}")


def cmd_adjudication(args):
    res = compare(args.labels_b)
    dis = set(res["citation_check"]["disagreements"]) | set(res["qa_citation"]["disagreements"]) | set(res["bad_item_flags"])
    A = load_labels(V3 / "labels" / "rater_a.jsonl")
    agreed = sorted(i for i in A if i not in dis and i not in res["missing_b"])
    k = max(1, round(0.10 * len(agreed)))
    audit = sorted(random.Random(SEED).sample(agreed, k))
    queue = {"disagreements_and_flags": sorted(dis), "audit_sample": audit}
    out = V3 / "labels" / f"adjudication_queue_round{args.round}.json"
    out.write_text(json.dumps(queue, indent=2) + "\n", encoding="utf-8")
    print(f"{len(dis)} disagreements/flags + {len(audit)} audit = {len(dis) + len(audit)} -> {out}")


# --------------------------------------------------------------------------- adjudication overlay
def cmd_apply_adjudication(_):
    """Overlay data/v0.3/labels/adjudicated.jsonl onto the assembled items (run after `assemble`).

    qa: ground_truth_chunks := final set (provenance.passage follows); cc: label := final label.
    Items rebuilt after adjudication (a `note` saying so, or a changed claim) keep their rebuilt label."""
    path = V3 / "labels" / "adjudicated.jsonl"
    adj = {r["id"]: r for r in jl_read(path)} if path.exists() else {}
    chunks = load_chunks()
    rebuilt = {i for i, r in adj.items() if "rewritten" in r.get("note", "")}
    rpath = V3 / "labels" / "relabel_v11.jsonl"
    relabel = {r["id"]: r for r in jl_read(rpath)} if rpath.exists() else {}
    changed = relabeled = 0
    for fname in ("qa_citation.jsonl", "citation_check.jsonl"):
        items = jl_read(V3 / fname)
        for it in items:
            r = adj.get(it["id"])
            if not r or it["id"] in rebuilt:
                continue
            if it["type"] == "qa_citation":
                final = sorted(r["final_label"], key=lambda c: int(c.split(":")[1]))
                assert set(final) <= set(it["candidate_window"]), it["id"]
                if final != it["ground_truth_chunks"]:
                    it["ground_truth_chunks"] = final
                    it["provenance"]["passage"] = "\n".join(chunks[c] for c in final)
                    changed += 1
            elif r["final_label"] != it["label"]:
                it["label"] = r["final_label"]
                changed += 1
            it["label_source"] = "adjudicated"
        for it in items:
            it.setdefault("label_source", "rater A = rater B (agreed)")
            # v1.1 single-rater re-label of the non-queued qa_citation items (AGREEMENT.md)
            rr = relabel.get(it["id"])
            if rr and it["type"] == "qa_citation" and it["label_source"] != "adjudicated":
                final = sorted(rr["label"], key=lambda c: int(c.split(":")[1]))
                if final and set(final) != set(it["ground_truth_chunks"]):
                    assert set(final) <= set(it["candidate_window"]), it["id"]
                    it["ground_truth_chunks"] = final
                    it["provenance"]["passage"] = "\n".join(chunks[c] for c in final)
                    it["label_source"] = "v1.1 re-label (changed)"
                    relabeled += 1
                else:
                    it["label_source"] = "rater A = rater B (agreed); confirmed under v1.1"
        jl_write(V3 / fname, items)
    print(f"applied {len(adj) - len(rebuilt)} adjudications ({changed} labels changed); {len(rebuilt)} rebuilt item(s) kept as rebuilt; "
          f"v1.1 re-label: {len(relabel)} items, {relabeled} changed")


# --------------------------------------------------------------------------- treatment
STATUSES = ("good law", "abrogated", "overruled", "unknown", "not_checked")
TREATMENT = V3 / "treatment.json"


def cmd_treatment_review(args):
    """Fold data/raw/treatment/<oid>.json screens into data/v0.3/treatment.json.

    Zero citing-with-negative-terms hits -> "good law" (screen basis). Any hit -> "unknown"
    until a human/curator entry with "reviewed": true sets the status; reviewed entries are kept."""
    raw = ROOT / "data" / "raw" / "treatment"
    cur = json.loads(TREATMENT.read_text()) if TREATMENT.exists() else {}
    pending = []
    for s in load_sources().values():
        oid = str(s["opinion_id"])
        if cur.get(oid, {}).get("reviewed"):
            continue
        path = raw / f"{oid}.json"
        if not path.exists():
            cur[oid] = {"precedential_status": "unknown", "reviewed": False, "basis": "not screened"}
            continue
        d = json.loads(path.read_text(encoding="utf-8"))
        req = json.loads((raw / f"{oid}.request.json").read_text())
        hits = [{"case_name": x["caseName"], "court_id": x["court_id"], "date_filed": x["dateFiled"],
                 "cluster_id": x["cluster_id"],
                 "snippet": re.sub(r"\s+", " ", " … ".join(o.get("snippet", "") for o in x["opinions"]))[:400]}
                for x in d["results"]]
        cur[oid] = {"precedential_status": "good law" if d["count"] == 0 else "unknown", "reviewed": False,
                    "screen_hits": d["count"], "screened_at": req["fetched_at"],
                    "basis": ("no CourtListener citing opinion uses abrogation/overruling/vacatur language"
                              if d["count"] == 0 else "citing opinions use negative-treatment terms; needs review"),
                    "hits": hits}
        if d["count"]:
            pending.append(oid)
    TREATMENT.write_text(json.dumps(dict(sorted(cur.items())), indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(Counter(v["precedential_status"] for v in cur.values())), "| needs review:", pending)


# --------------------------------------------------------------------------- markdown renderers
def agreement_tables(res):
    cc, qa = res["citation_check"], res["qa_citation"]
    lines = ["| Type | n | Percent agreement | Cohen's kappa | Notes |", "|---|---|---|---|---|",
             f"| `citation_check` | {cc['n']} | {cc['percent_agreement']:.1%} | {cc['kappa']:.3f} | 4-way label |",
             f"| `qa_citation` | {qa['n']} | {qa['exact_set_agreement']:.1%} (exact chunk set) | {qa['chunk_kappa']:.3f} (chunk-level, "
             f"{qa['chunk_decisions']} decisions) | chunk-level agreement {qa['chunk_percent_agreement']:.1%}; mean Jaccard {qa['mean_jaccard']:.3f} |",
             "", "`citation_check` confusion (rows = rater A, columns = rater B):", "",
             "| A \\ B | " + " | ".join(CC_LABELS) + " |", "|---|" + "---|" * len(CC_LABELS)]
    for a in CC_LABELS:
        row = cc["confusion_a_rows_b_cols"].get(a, {})
        lines.append(f"| {a} | " + " | ".join(str(row.get(b, 0)) for b in CC_LABELS) + " |")
    return "\n".join(lines)


def cmd_render(args):
    """Write agreement tables + the adjudication checklist for a round."""
    res = compare(args.labels_b)
    (V3 / "labels" / f"agreement_tables_round{args.round}.md").write_text(agreement_tables(res) + "\n", encoding="utf-8")
    queue = json.loads((V3 / "labels" / f"adjudication_queue_round{args.round}.json").read_text())
    recs = json.loads((V3 / "labels" / f"recommendations_round{args.round}.json").read_text())
    chunks = load_chunks()
    items = {it["id"]: it for it in jl_read(V3 / "qa_citation.jsonl") + jl_read(V3 / "citation_check.jsonl")}
    A, B = load_labels(V3 / "labels" / "rater_a.jsonl"), load_labels(args.labels_b)

    def block(cid):
        return f"`{cid}`\n\n> " + chunks[cid].replace("\n", "\n>\n> ")

    out = []
    for section, ids in (("Disagreements and bad-item flags", queue["disagreements_and_flags"]),
                         ("Random 10% audit of agreed items", queue["audit_sample"])):
        out.append(f"## {section} ({len(ids)})\n")
        for i in ids:
            it, a, b, r = items[i], A[i], B[i], recs.get(i, {})
            prov = it["provenance"]
            out.append(f"### [ ] {i} · {it['type']} · {prov['case_name']} ({prov['court_id']}, {prov['date_filed']})\n")
            out.append(f"Source: [{prov['url']}]({prov['url']}) · opinion {prov['opinion_id']} · cited authority as it appears: `{prov['cited_authority']}`\n")
            if it["type"] == "qa_citation":
                out.append(f"**Question:** {it['question']}\n\n**Reference notes:** {it['reference_notes']}\n")
                shown = sorted(set(a["label"]) | set(b["label"] or []), key=lambda c: int(c.split(':')[1]))
                out.append("**Chunks either rater chose:**\n\n" + "\n\n".join(block(c) for c in shown) + "\n")
                out.append(f"Candidate window: {', '.join(f'`{c}`' for c in it['candidate_window'])}\n")
            else:
                out.append(f"**Claim:** {it['claim']}\n\n**Cited passage:** {block(it['cited_chunk'])}\n")
                others = [c for c in it["context_chunks"] if c != it["cited_chunk"]]
                out.append("<details><summary>Other passages available</summary>\n\n" + "\n\n".join(block(c) for c in others) + "\n\n</details>\n")
            out.append(f"| | Label | Reason |\n|---|---|---|\n| Rater A | `{a['label']}` | {a['reason']} |\n| Rater B | `{b['label']}` | {b['reason']}"
                       + (f" **bad_item:** {b['bad_item']}" if b.get("bad_item") else "") + " |\n")
            out.append(f"**Recommended:** `{r.get('label', '?')}` — {r.get('why', '')}\n\n**Final label:** ______\n\n---\n")
    (V3 / "labels" / f"adjudication_body_round{args.round}.md").write_text("\n".join(out), encoding="utf-8")
    print(f"rendered {len(queue['disagreements_and_flags']) + len(queue['audit_sample'])} queue items")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["packets", "assemble", "validate", "rater-input", "agreement", "adjudication", "render", "import-labels", "treatment-review", "apply-adjudication"])
    ap.add_argument("--labels-b", default=str(V3 / "labels" / "rater_b_round1.jsonl"))
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--out", default=None, help="rater-input: write batches here (e.g. an isolated scratch dir)")
    ap.add_argument("--src", default=None, help="import-labels: rater output file (opaque ids)")
    ap.add_argument("--append", action="store_true", help="import-labels: merge into an existing round file")
    args = ap.parse_args()
    {"packets": cmd_packets, "assemble": cmd_assemble, "validate": cmd_validate, "rater-input": cmd_rater_input,
     "agreement": cmd_agreement, "adjudication": cmd_adjudication, "render": cmd_render, "import-labels": cmd_import_labels, "treatment-review": cmd_treatment_review, "apply-adjudication": cmd_apply_adjudication}[args.cmd](args)


if __name__ == "__main__":
    main()
