"""Fetch v0.3 candidate opinions from the CourtListener REST API v4.

`search`: one REST v4 search per topic in data/v0.3/topics.json, first page
saved byte-exact to data/raw/search/<topic_key>.json (request params and time in
<topic_key>.request.json). Queries were first explored with the CourtListener MCP.

`fetch`: takes those candidates in rank order and, per topic, fetches opinions
until it has --per-topic that pass the source rules in LABELING_PROTOCOL.md §2:

  GET /api/rest/v4/opinions/<id>/   -> data/raw/opinions/<id>.json        (verbatim)
  cluster metadata (case name, date filed, precedential status, URL) is taken from
  the verbatim search response; data/raw/clusters/ holds the few clusters fetched early
  accepted                          -> data/raw/opinions/<id>.meta.json   (provenance)
  every decision                    -> data/v0.3/work/fetch_log.jsonl

Requires COURTLISTENER_API_TOKEN in the environment (never written anywhere).
Cached responses are reused, so re-runs cost no requests. Requests are spaced
by --delay seconds and 429s honour Retry-After.

Usage:  python src/v03_fetch.py search [--topics a,b]
        python src/v03_fetch.py fetch [--per-topic 3] [--delay 1.0] [--topics a,b]
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import hashlib

import requests

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
V3 = ROOT / "data" / "v0.3"
API = "https://www.courtlistener.com/api/rest/v4"
STORAGE = "https://storage.courtlistener.com"

# search returns display names, the REST opinion endpoint returns codes ("015unamimous" is CourtListener's spelling)
ALLOWED_TYPES = {"combined-opinion", "lead-opinion", "majority-opinion", "unanimous-opinion",
                 "010combined", "015unamimous", "020lead"}
TEXT_FIELDS = ("plain_text", "html_with_citations", "html", "html_lawbox", "html_columbia", "xml_harvard")
MIN_WORDS, MAX_CHARS = 1500, 80000
EXCLUDE_NAME_RE = re.compile(r"in re (the )?marriage|adoption|juvenile|custody|guardianship|disciplinary|"
                             r"\bin re [a-z]\.\s?[a-z]\.|\binstead\b", re.I)
EXCLUDE_TEXT_RE = re.compile(r"sexual(ly)? assault|\brape\b|child pornography|sex offender|minor victim|"
                             r"sexual abuse|sexual activity|termination of parental rights|divorce decree|dissolution of marriage|"
                             r"\b([1-9]|1[0-7])-year-old|\bchildren (died|were killed)", re.I)
# the opening of the text must be a court-of-last-resort / circuit majority, not a dissent, order or trial-court opinion
HEAD_REJECT_RE = re.compile(r"DISSENTING OPINION|CONCURRING OPINION|OPINION IN SUPPORT OF (AFFIRMANCE|REVERSAL)|"
                            r"\bOn order of the Court\b|MEMORANDUM OPINION|"
                            r"\bPls?\.[’'] (Mem|Opp|Mot)\.", re.I)
FEDERAL_APPEALS_RE = re.compile(r"Circuit Judges?|COURT OF APPEALS", re.I)


class Client:
    def __init__(self, token, delay):
        self.s = requests.Session()
        self.s.headers.update({"Authorization": f"Token {token}", "User-Agent": "crosssource-v0.3 (research; MIT)"})
        self.delay, self.requests = delay, 0

    def request(self, path, params=None):
        for _ in range(8):
            time.sleep(self.delay)
            try:
                r = self.s.get(f"{API}/{path}", params=params, timeout=90)
            except (requests.ConnectionError, requests.Timeout) as e:
                print(f"    {type(e).__name__} on {path} — retrying in 30s")
                time.sleep(30)
                continue
            self.requests += 1
            if r.status_code >= 500:
                print(f"    {r.status_code} on {path} — retrying in 30s")
                time.sleep(30)
                continue
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", "60"))
                print(f"    429 on {path} — waiting {wait}s")
                time.sleep(wait)
                continue
            r.raise_for_status()
            return r
        raise RuntimeError(f"rate-limited 8 times on {path}")

    def get(self, path, cache):
        if cache.exists():
            return json.loads(cache.read_text(encoding="utf-8"))
        r = self.request(path)
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(r.content)
        return r.json()


def storage_pdf_opinion(storage, result, oid):
    """Opinion text from CourtListener's public file storage instead of the API (no API quota).

    The PDF is cached at data/raw/pdf/<oid>.pdf and must match the sha1 that the
    verbatim REST search response lists for that opinion."""
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from v03_corpus import pdf_text
    o = next(o for o in result["opinions"] if o["id"] == oid)
    if not (o.get("local_path") or "").endswith(".pdf") or not o.get("sha1"):
        return None, "no storage PDF listed"
    path = RAW / "pdf" / f"{oid}.pdf"
    if not path.exists():
        time.sleep(1.0)
        r = storage.get(f"{STORAGE}/{o['local_path']}", timeout=90)
        r.raise_for_status()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(r.content)
    digest = hashlib.sha1(path.read_bytes()).hexdigest()
    if digest != o["sha1"]:
        return None, f"sha1 mismatch ({digest[:10]} != {o['sha1'][:10]})"
    op = {"id": oid, "type": o.get("type"), "per_curiam": o.get("per_curiam"), "plain_text": pdf_text(path),
          "_pdf_url": f"{STORAGE}/{o['local_path']}", "_sha1": digest}
    return op, None


def search_params(topic):
    return {"type": "o", "q": topic["q"], "court": " ".join(topic["courts"]), "filed_after": "2018-01-01",
            "stat_Published": "on", "order_by": "score desc"}


def cmd_search(client, topics):
    for topic in topics:
        params = search_params(topic)
        out = RAW / "search" / f"{topic['topic_key']}.json"
        if out.exists() and (RAW / "search" / f"{topic['topic_key']}.request.json").exists():
            continue
        r = client.request("search/", params)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(r.content)
        (RAW / "search" / f"{topic['topic_key']}.request.json").write_text(json.dumps(
            {"url": f"{API}/search/", "params": params, "status": r.status_code,
             "fetched_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}, indent=2) + "\n")
        d = r.json()
        print(f"{topic['topic_key']:28} count={d['count']:5}  page={len(d['results'])}  "
              f"courts={sorted({x['court_id'] for x in d['results']})}")


def opinion_text(op):
    for f in TEXT_FIELDS:
        if (op.get(f) or "").strip():
            return f, op[f]
    return None, ""


EXCLUSIONS = json.loads((V3 / "exclusions.json").read_text(encoding="utf-8")) if (V3 / "exclusions.json").exists() else {}


def check(result, op, cluster, topic):
    """Return None if the opinion passes §2, else the reason it fails."""
    if str(op.get("id")) in EXCLUSIONS:
        return f"manual exclusion: {EXCLUSIONS[str(op['id'])]}"
    if result["court_id"] not in topic["courts"]:
        return f"court {result['court_id']} not in topic list"
    if cluster.get("precedential_status") != "Published":
        return f"precedential_status {cluster.get('precedential_status')}"
    if (cluster.get("date_filed") or "") < "2018-01-01":
        return f"date_filed {cluster.get('date_filed')}"
    if op.get("type") not in ALLOWED_TYPES:
        return f"opinion type {op.get('type')}"
    if op.get("per_curiam"):
        return "per curiam"
    name = cluster.get("case_name") or result["caseName"]
    if EXCLUDE_NAME_RE.search(name):
        return f"excluded case type by name: {name}"
    field, text = opinion_text(op)
    if not field:
        return "no opinion text"
    plain = re.sub(r"<[^>]+>", " ", text)
    if len(plain.split()) < MIN_WORDS:
        return f"too short ({len(plain.split())} words)"
    if len(plain) > MAX_CHARS:
        return f"too long ({len(plain)} chars)"
    m = EXCLUDE_TEXT_RE.search(plain)
    if m:
        return f"excluded subject matter: {m.group(0)!r}"
    m = HEAD_REJECT_RE.search(plain[:3000])
    if m:
        return f"not a majority appellate opinion: {m.group(0)!r}"
    if re.fullmatch(r"ca\d+|cadc|cafc", result["court_id"]) and not FEDERAL_APPEALS_RE.search(plain[:6000]):
        return "tagged as a court of appeals but the text reads as a trial-court opinion"
    return None


def candidates(topic):
    path = RAW / "search" / f"{topic['topic_key']}.json"
    if not path.exists():
        return None
    out, seen = [], set()
    for r in json.loads(path.read_text(encoding="utf-8"))["results"]:
        if r["cluster_id"] in seen or r.get("status") != "Published":
            continue
        seen.add(r["cluster_id"])
        lead = [o for o in r.get("opinions") or r.get("cluster_opinions") or [] if o.get("type") in ALLOWED_TYPES]
        if lead:
            out.append((r, lead[0]["id"]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["search", "fetch"])
    ap.add_argument("--per-topic", type=int, default=3)
    ap.add_argument("--delay", type=float, default=1.0)
    ap.add_argument("--topics", default="")
    ap.add_argument("--source", choices=["api", "pdf"], default="api",
                    help="fetch: opinion text from the REST API, or from CourtListener's storage PDFs (sha1-verified)")
    args = ap.parse_args()
    token = os.environ.get("COURTLISTENER_API_TOKEN")
    if not token:
        sys.exit("COURTLISTENER_API_TOKEN is not set")
    topics = json.loads((V3 / "topics.json").read_text(encoding="utf-8"))
    if args.topics:
        topics = [t for t in topics if t["topic_key"] in args.topics.split(",")]
    client = Client(token, args.delay)
    storage = requests.Session()
    storage.headers["User-Agent"] = "crosssource-v0.3 (research; MIT)"
    if args.cmd == "search":
        cmd_search(client, topics)
        print(f"\n{client.requests} API requests this run")
        return
    log_path = V3 / "work" / "fetch_log.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log = open(log_path, "a", encoding="utf-8")
    summary = {}

    for topic in topics:
        cands = candidates(topic)
        if cands is None:
            print(f"[{topic['topic_key']}] no cached search — run `search` first")
            continue
        metas = [json.loads(p.read_text()) for p in (RAW / "opinions").glob("*.meta.json")]
        accepted = [m["opinion_id"] for m in metas if m.get("topic_key") == topic["topic_key"]]
        # CourtListener sometimes holds one decision under two clusters; dedupe on name + date
        same_case = {(m["case_name"].lower(), m["date_filed"]) for m in metas}
        courts_used = set()
        # two passes: first prefer one opinion per court, then fill
        for distinct in (True, False):
            for result, oid in cands:
                if len(accepted) >= args.per_topic:
                    break
                if oid in accepted or (distinct and result["court_id"] in courts_used):
                    continue
                if result["court_id"] not in topic["courts"] or EXCLUDE_NAME_RE.search(result["caseName"]):
                    continue  # decided from search metadata alone; no request spent
                if (result["caseName"].lower(), result["dateFiled"]) in same_case:
                    continue  # duplicate cluster of a case already accepted
                if args.source == "pdf":
                    op, why = storage_pdf_opinion(storage, result, oid)
                    if op is None:
                        print(f"  - {oid} {result['caseName'][:50]}: {why}")
                        continue
                else:
                    op = client.get(f"opinions/{oid}/", RAW / "opinions" / f"{oid}.json")
                # cluster metadata comes from the verbatim search response (same fields as clusters/<id>/),
                # which halves the requests against CourtListener's 50/hour, 125/day quota
                cached = RAW / "clusters" / f"{result['cluster_id']}.json"
                cluster = (json.loads(cached.read_text(encoding="utf-8")) if cached.exists() else
                           {"case_name": result["caseName"], "date_filed": result["dateFiled"],
                            "precedential_status": result["status"], "absolute_url": result["absolute_url"]})
                reason = check(result, op, cluster, topic)
                entry = {"topic_key": topic["topic_key"], "opinion_id": oid, "cluster_id": result["cluster_id"],
                         "case_name": result["caseName"], "court_id": result["court_id"], "accepted": reason is None,
                         "reason": reason, "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
                log.write(json.dumps(entry) + "\n")
                log.flush()
                if reason:
                    print(f"  - {oid} {result['caseName'][:50]}: {reason}")
                    continue
                field, _ = opinion_text(op)
                meta = {
                    "opinion_id": oid, "cluster_id": result["cluster_id"],
                    "case_name": cluster.get("case_name") or result["caseName"],
                    "court_id": result["court_id"], "date_filed": cluster.get("date_filed"),
                    "citation": result.get("citation") or [], "docket_number": result.get("docketNumber"),
                    "absolute_url": cluster.get("absolute_url") or result["absolute_url"],
                    "url": "https://www.courtlistener.com" + (cluster.get("absolute_url") or result["absolute_url"]),
                    "api_url": f"{API}/opinions/{oid}/", "opinion_type": op.get("type"),
                    "per_curiam": op.get("per_curiam"),
                    "text_field": "storage_pdf" if args.source == "pdf" else field,
                    **({"pdf_url": op["_pdf_url"], "pdf_sha1": op["_sha1"]} if args.source == "pdf" else {}),
                    "precedential_status": cluster.get("precedential_status"),
                    "topic_key": topic["topic_key"], "area_of_law": topic["area_of_law"],
                    "fetched_at": entry["at"],
                }
                (RAW / "opinions" / f"{oid}.meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
                accepted.append(oid)
                same_case.add((meta["case_name"].lower(), meta["date_filed"]))
                courts_used.add(result["court_id"])
                print(f"  + {oid} {result['court_id']:5} {meta['date_filed']} {meta['case_name'][:50]} [{field}]")
        summary[topic["topic_key"]] = len(accepted)
        print(f"[{topic['topic_key']}] {len(accepted)}/{args.per_topic} accepted")

    print(f"\n{client.requests} API requests this run")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
