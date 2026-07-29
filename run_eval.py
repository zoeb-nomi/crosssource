"""Run the full CrossSource evaluation: every golden item x both configurations.

Writes per-item raw results to results/raw_results.jsonl and an aggregate
summary to results/summary.json.

Results are appended to results/raw_results.jsonl as each evaluation
completes, so an interrupted run loses at most the in-flight items;
--resume skips (item, config) pairs already present in that file.

Usage:
  python run_eval.py             # full golden set, both configs
  python run_eval.py --limit 2   # smoke test on the first N items
  python run_eval.py --resume    # continue an interrupted run
"""

import argparse
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

import anthropic
from dotenv import load_dotenv

from evaluate import eval_item
from generate import CONFIGS, answer
from retrieval import Retriever

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"


def run_one(client, retriever, item, config):
    generation = answer(item["question"], config, retriever, client)
    retrieved_chunks = [retriever.get(cid) for cid in generation["retrieved"]]
    return eval_item(client, item, generation, retrieved_chunks)


def aggregate(rows, config):
    sub = [r for r in rows if r["config"] == config]
    n = len(sub)
    if not n:
        return {}
    labels = {}
    for r in sub:
        for j in r["citation_judgments"]:
            if not j["supported"]:
                labels[j["failure_label"]] = labels.get(j["failure_label"], 0) + 1
        if r["missing_authority"]:
            labels["missing_authority"] = labels.get("missing_authority", 0) + len(r["missing_authority"])
    return {
        "items": n,
        "citation_precision": round(sum(r["citation_precision"] for r in sub) / n, 4),
        "citation_recall": round(sum(r["citation_recall"] for r in sub) / n, 4),
        "faithfulness": round(sum(r["faithfulness"] for r in sub) / n, 4),
        "relevance": round(sum(r["relevance"] for r in sub) / n, 4),
        "failure_labels": labels,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="run only the first N golden items")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--resume", action="store_true", help="skip pairs already in results/raw_results.jsonl")
    args = parser.parse_args()

    load_dotenv()
    golden = [json.loads(ln) for ln in (ROOT / "data" / "golden.jsonl").read_text().splitlines() if ln.strip()]
    if args.limit:
        golden = golden[: args.limit]

    RESULTS.mkdir(exist_ok=True)
    out = RESULTS / "raw_results.jsonl"
    rows = []
    if args.resume and out.exists():
        rows = [json.loads(ln) for ln in out.read_text().splitlines() if ln.strip()]
    done = {(r["id"], r["config"]) for r in rows}

    retriever = Retriever()
    client = anthropic.Anthropic()
    jobs = [(item, config) for item in golden for config in CONFIGS if (item["id"], config) not in done]
    print(f"{len(golden)} items x {len(CONFIGS)} configs = {len(jobs)} to run ({len(done)} already done)")

    write_lock = threading.Lock()
    failures = []
    with open(out, "a" if args.resume else "w", encoding="utf-8") as fh:
        if not args.resume:
            rows = []
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {pool.submit(run_one, client, retriever, item, config): (item["id"], config) for item, config in jobs}
            for future in as_completed(futures):
                item_id, config = futures[future]
                try:
                    row = future.result()
                    with write_lock:
                        rows.append(row)
                        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
                        fh.flush()
                    print(f"  done {item_id}/{config} ({len(rows)}/{len(jobs) + len(done)})")
                except Exception as e:
                    failures.append((item_id, config, str(e)))
                    print(f"  FAILED {item_id}/{config}: {e}")

    rows.sort(key=lambda r: (r["id"], r["config"]))
    out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")

    summary = {config: aggregate(rows, config) for config in CONFIGS}
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    print(f"\nwrote {out} ({len(rows)} rows) and results/summary.json")
    for config, s in summary.items():
        print(f"\n[{config}] precision={s['citation_precision']} recall={s['citation_recall']} "
              f"faithfulness={s['faithfulness']} relevance={s['relevance']}")
        print(f"  failure labels: {s['failure_labels'] or 'none'}")
    if failures:
        print(f"\n{len(failures)} evaluations failed: {failures}")
        sys.exit(1)


if __name__ == "__main__":
    main()
