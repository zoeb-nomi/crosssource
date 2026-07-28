"""Validate data/golden.jsonl (the human-authored golden set).

Each line must be a JSON object:
  {
    "id": "g01",
    "question": "...",
    "reference_notes": "...",
    "ground_truth_chunks": ["doc_id:chunk_id", ...]
  }

Checks: unique ids, non-empty fields, every ground-truth chunk exists in the
current (deterministic) chunking, and >= 25 items for the milestone bar.

Usage:  python src/golden_check.py
"""

import json
import sys
from pathlib import Path

from retrieval import Retriever

GOLDEN = Path(__file__).resolve().parent.parent / "data" / "golden.jsonl"
REQUIRED = {"id", "question", "reference_notes", "ground_truth_chunks"}


def main():
    if not GOLDEN.exists():
        sys.exit(f"{GOLDEN} does not exist yet (M3 not started)")

    retriever = Retriever()
    valid_ids = {c["id"] for c in retriever.chunks}
    errors, seen = [], set()

    lines = [ln for ln in GOLDEN.read_text(encoding="utf-8").splitlines() if ln.strip()]
    for n, line in enumerate(lines, 1):
        try:
            item = json.loads(line)
        except json.JSONDecodeError as e:
            errors.append(f"line {n}: invalid JSON ({e})")
            continue
        missing = REQUIRED - item.keys()
        if missing:
            errors.append(f"line {n}: missing fields {sorted(missing)}")
            continue
        if item["id"] in seen:
            errors.append(f"line {n}: duplicate id {item['id']}")
        seen.add(item["id"])
        if not item["question"].strip() or not item["reference_notes"].strip():
            errors.append(f"line {n} ({item['id']}): empty question or notes")
        if not item["ground_truth_chunks"]:
            errors.append(f"line {n} ({item['id']}): no ground-truth chunks")
        for cid in item["ground_truth_chunks"]:
            if cid not in valid_ids:
                errors.append(f"line {n} ({item['id']}): unknown chunk id {cid}")

    print(f"{len(lines)} items")
    if len(lines) < 25:
        errors.append(f"only {len(lines)} items — milestone requires >= 25")
    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("golden.jsonl validates: OK")


if __name__ == "__main__":
    main()
