"""Validate data/sources.json against data/corpus/ and print corpus stats.

Checks: every corpus file has a sources entry and vice versa, required
provenance fields are present, no tax cases (out of scope, see README),
and total size stays under 3 MB.

Usage:  python src/corpus_stats.py
"""

import json
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
REQUIRED_FIELDS = {"file", "case_name", "citation", "court", "source", "url"}
TAX_MARKERS = ("tax", "internal revenue", "commissioner of internal", "irs")


def main():
    sources = json.loads((DATA / "sources.json").read_text(encoding="utf-8"))
    corpus_files = {p.name for p in (DATA / "corpus").glob("*.txt")}
    listed_files = {e["file"] for e in sources}

    errors = []
    if corpus_files - listed_files:
        errors.append(f"files missing from sources.json: {sorted(corpus_files - listed_files)}")
    if listed_files - corpus_files:
        errors.append(f"sources.json entries with no file: {sorted(listed_files - corpus_files)}")
    for e in sources:
        missing = REQUIRED_FIELDS - e.keys()
        if missing:
            errors.append(f"{e.get('file', '?')}: missing fields {sorted(missing)}")
        if any(m in e["case_name"].lower() for m in TAX_MARKERS):
            errors.append(f"{e['file']}: tax case detected — out of scope")

    total_chars = 0
    print(f"{'file':<36} {'chars':>9} {'~tokens':>9}  case")
    for e in sorted(sources, key=lambda x: x["file"]):
        chars = len((DATA / "corpus" / e["file"]).read_text(encoding="utf-8"))
        total_chars += chars
        print(f"{e['file']:<36} {chars:>9,} {chars // 4:>9,}  {e['case_name']}")

    print(f"\ndocs: {len(sources)}   total: {total_chars / 1e6:.2f} MB   ~tokens: {total_chars // 4:,}")

    if total_chars > 3_000_000:
        errors.append(f"corpus exceeds 3 MB budget ({total_chars / 1e6:.2f} MB)")
    if not 15 <= len(sources) <= 25:
        errors.append(f"doc count {len(sources)} outside 15-25 range")

    if errors:
        print("\nVALIDATION FAILED:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    print("sources.json validates: OK")


if __name__ == "__main__":
    main()
