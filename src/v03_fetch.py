"""Fetch v0.3 candidate opinions from the CourtListener REST API v4.

Discovery is done separately (CourtListener MCP `search`, one response per
topic saved to data/raw/search/<topic_key>.json). This script takes those
candidates in rank order and, per topic, fetches opinions until it has
--per-topic that pass the source rules in LABELING_PROTOCOL.md §2:

  GET /api/rest/v4/opinions/<id>/   -> data/raw/opinions/<id>.json        (verbatim)
  GET /api/rest/v4/clusters/<id>/   -> data/raw/clusters/<id>.json        (verbatim)
  accepted                          -> data/raw/opinions/<id>.meta.json   (provenance)
  every decision                    -> data/v0.3/work/fetch_log.jsonl

Requires COURTLISTENER_API_TOKEN in the environment (never written anywhere).
Cached responses are reused, so re-runs cost no requests. Requests are spaced
by --delay seconds and 429s honour Retry-After.

Usage:  python src/v03_fetch.py [--per-topic 3] [--delay 1.0] [--topics a,b]
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
V3 = ROOT / "data" / "v0.3"
API = "https://www.courtlistener.com/api/rest/v4"

# search returns display names, the REST opinion endpoint returns codes ("015unamimous" is CourtListener's spelling)
ALLOWED_TYPES = {"combined-opinion", "lead-opinion", "majority-opinion", "unanimous-opinion",
                 "010combined", "015unamimous", "020lead"}
TEXT_FIELDS = ("plain_text", "html_with_citations", "html", "html_lawbox", "html_columbia", "xml_harvard")
MIN_WORDS, MAX_CHARS = 1500, 80000
EXCLUDE_NAME_RE = re.compile(r"in re (the )?marriage|adoption|juvenile|custody|guardianship|disciplinary|"
                             r"\bin re [a-z]\.\s?[a-z]\.|\binstead\b", re.I)
EXCLUDE_TEXT_RE = re.compile(r"sexual(ly)? assault|\brape\b|child pornography|sex offender|minor victim|"
                             r"sexual abuse|termination of parental rights", re.I)


class Client:
    def __init__(self, token, delay):
        self.s = requests.Session()
        self.s.headers.update({"Authorization": f"Token {token}", "User-Agent": "crosssource-v0.3 (research; MIT)"})
        self.delay, self.requests = delay, 0

    def get(self, path, cache):
        if cache.exists():
            return json.loads(cache.read_text(encoding="utf-8"))
        for _ in range(5):
            time.sleep(self.delay)
            r = self.s.get(f"{API}/{path}", timeout=60)
            self.requests += 1
            if r.status_code == 429:
                wait = int(r.headers.get("Retry-After", "60"))
                print(f"    429 — waiting {wait}s")
                time.sleep(wait)
                continue
            r.raise_for_status()
            cache.parent.mkdir(parents=True, exist_ok=True)
            cache.write_text(r.text, encoding="utf-8")
            return r.json()
        raise RuntimeError(f"rate-limited 5 times on {path}")


def opinion_text(op):
    for f in TEXT_FIELDS:
        if (op.get(f) or "").strip():
            return f, op[f]
    return None, ""


def check(result, op, cluster, topic):
    """Return None if the opinion passes §2, else the reason it fails."""
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
    ap.add_argument("--per-topic", type=int, default=3)
    ap.add_argument("--delay", type=float, default=1.0)
    ap.add_argument("--topics", default="")
    args = ap.parse_args()
    token = os.environ.get("COURTLISTENER_API_TOKEN")
    if not token:
        sys.exit("COURTLISTENER_API_TOKEN is not set")
    topics = json.loads((V3 / "topics.json").read_text(encoding="utf-8"))
    if args.topics:
        topics = [t for t in topics if t["topic_key"] in args.topics.split(",")]
    client = Client(token, args.delay)
    log_path = V3 / "work" / "fetch_log.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log = open(log_path, "a", encoding="utf-8")
    summary = {}

    for topic in topics:
        cands = candidates(topic)
        if cands is None:
            print(f"[{topic['topic_key']}] no cached search — run the MCP search first")
            continue
        accepted = [json.loads(p.read_text())["opinion_id"] for p in (RAW / "opinions").glob("*.meta.json")
                    if json.loads(p.read_text()).get("topic_key") == topic["topic_key"]]
        courts_used = set()
        # two passes: first prefer one opinion per court, then fill
        for distinct in (True, False):
            for result, oid in cands:
                if len(accepted) >= args.per_topic:
                    break
                if oid in accepted or (distinct and result["court_id"] in courts_used):
                    continue
                if result["court_id"] not in topic["courts"]:
                    continue
                op = client.get(f"opinions/{oid}/", RAW / "opinions" / f"{oid}.json")
                cluster = client.get(f"clusters/{result['cluster_id']}/", RAW / "clusters" / f"{result['cluster_id']}.json")
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
                    "per_curiam": op.get("per_curiam"), "text_field": field,
                    "precedential_status": cluster.get("precedential_status"),
                    "topic_key": topic["topic_key"], "area_of_law": topic["area_of_law"],
                    "fetched_at": entry["at"],
                }
                (RAW / "opinions" / f"{oid}.meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
                accepted.append(oid)
                courts_used.add(result["court_id"])
                print(f"  + {oid} {result['court_id']:5} {meta['date_filed']} {meta['case_name'][:50]} [{field}]")
        summary[topic["topic_key"]] = len(accepted)
        print(f"[{topic['topic_key']}] {len(accepted)}/{args.per_topic} accepted")

    print(f"\n{client.requests} API requests this run")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
