"""Run the CrossSource evaluation.

v0.1 (default): every golden item x both configurations, as published.
v0.3: qa_citation items run through retrieve -> generate -> judge exactly as in
v0.1, over the v0.3 corpus; citation_check items ask the model under test to
make the citation-precision judge's decision and score it against the
adjudicated label (accuracy + Cohen's kappa).

Results are appended to <out>/raw_results.jsonl as each evaluation completes,
so an interrupted run loses at most the in-flight items; --resume skips
(item, config) pairs already present. Token usage and $ cost go to
<out>/summary.json.

Usage:
  python run_eval.py                                  # v0.1, as published
  python run_eval.py --limit 2                        # v0.1 smoke test
  python run_eval.py --dataset v0.3 --model claude-sonnet-5-5 --sample 30
  python run_eval.py --dataset v0.3 --model gpt-5-mini --judge-model claude-sonnet-5-5 --sample 30
"""

import argparse
import json
import random
import re
import sys
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from dotenv import load_dotenv

import llm
from evaluate import JUDGE_MODEL, eval_item, judge_citation
from generate import CONFIGS, MODEL, answer
from retrieval import Retriever

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "results"
SAMPLE_SEED = 20261019


def run_qa(retriever, item, config, model, judge_model):
    generation = answer(item["question"], config, retriever, model=model)
    retrieved_chunks = [retriever.get(cid) for cid in generation["retrieved"]]
    row = eval_item(item, generation, retrieved_chunks, judge_model=judge_model)
    return {**row, "type": "qa_citation", "model": model}


def run_cc(retriever, item, model):
    cited = retriever.get(item["cited_chunk"])
    others = [retriever.get(c) for c in item["context_chunks"] if c != item["cited_chunk"]]
    v = judge_citation(model, item["claim"], cited, others)
    pred = "supported" if v["supported"] else v["failure_label"]
    if pred == "none":  # unsupported but no failure class given
        pred = "unsupported_claim"
    return {"id": item["id"], "config": "judge", "type": "citation_check", "model": model,
            "gold": item["label"], "pred": pred, "correct": pred == item["label"], "reason": v["reason"]}


def aggregate_qa(rows, config):
    sub = [r for r in rows if r["config"] == config and r.get("type", "qa_citation") == "qa_citation"]
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


def aggregate_cc(rows):
    from v03_dataset import cohen_kappa
    sub = [r for r in rows if r.get("type") == "citation_check"]
    if not sub:
        return {}
    gold, pred = [r["gold"] for r in sub], [r["pred"] for r in sub]
    return {"items": len(sub), "accuracy": round(sum(r["correct"] for r in sub) / len(sub), 4),
            "kappa": round(cohen_kappa(gold, pred), 4),
            "confusion_gold_rows_pred_cols": {g: dict(Counter(p for gg, p in zip(gold, pred) if gg == g)) for g in sorted(set(gold))}}


def load_v03(sample):
    v3 = ROOT / "data" / "v0.3"
    qa = [json.loads(ln) for ln in (v3 / "qa_citation.jsonl").read_text().splitlines() if ln.strip()]
    cc = [json.loads(ln) for ln in (v3 / "citation_check.jsonl").read_text().splitlines() if ln.strip()]
    if sample:
        rng = random.Random(SAMPLE_SEED)
        qa = rng.sample(qa, min(len(qa), sample // 2))
        cc = rng.sample(cc, min(len(cc), sample - len(qa)))
    return qa, cc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", choices=["v0.1", "v0.3"], default="v0.1")
    parser.add_argument("--model", default=MODEL, help="model under test (Anthropic id, or gpt-* / openai:<id>)")
    parser.add_argument("--judge-model", default=JUDGE_MODEL, help="judge for qa_citation scoring (kept fixed across models)")
    parser.add_argument("--configs", default=",".join(CONFIGS), help="comma-separated generation configs")
    parser.add_argument("--sample", type=int, default=None, help="v0.3: seeded sample of N items, half per type")
    parser.add_argument("--limit", type=int, default=None, help="v0.1: run only the first N golden items")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--out", default=None)
    parser.add_argument("--resume", action="store_true", help="skip pairs already in <out>/raw_results.jsonl")
    args = parser.parse_args()

    load_dotenv()
    configs = [c for c in args.configs.split(",") if c]
    if args.dataset == "v0.1":
        golden = [json.loads(ln) for ln in (ROOT / "data" / "golden.jsonl").read_text().splitlines() if ln.strip()]
        qa, cc = golden[: args.limit] if args.limit else golden, []
        retriever = Retriever()
        out_dir = Path(args.out) if args.out else RESULTS
    else:
        qa, cc = load_v03(args.sample)
        retriever = Retriever(ROOT / "data" / "v0.3" / "corpus")
        slug = re.sub(r"[^a-z0-9.-]+", "_", args.model.lower())
        out_dir = Path(args.out) if args.out else RESULTS / "v0.3" / slug

    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "raw_results.jsonl"
    rows = []
    if args.resume and out.exists():
        rows = [json.loads(ln) for ln in out.read_text().splitlines() if ln.strip()]
    done = {(r["id"], r["config"]) for r in rows}

    jobs = [("qa", item, c) for item in qa for c in configs if (item["id"], c) not in done]
    jobs += [("cc", item, "judge") for item in cc if (item["id"], "judge") not in done]
    print(f"{args.dataset}: {len(qa)} qa x {len(configs)} configs + {len(cc)} citation_check = {len(jobs)} to run "
          f"({len(done)} already done); model={args.model} judge={args.judge_model}")

    write_lock = threading.Lock()
    failures = []
    with open(out, "a" if args.resume else "w", encoding="utf-8") as fh:
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = {}
            for kind, item, config in jobs:
                f = (pool.submit(run_qa, retriever, item, config, args.model, args.judge_model) if kind == "qa"
                     else pool.submit(run_cc, retriever, item, args.model))
                futures[f] = (item["id"], config)
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

    summary = {config: aggregate_qa(rows, config) for config in configs}
    if args.dataset == "v0.3":
        summary = {"model": args.model, "judge_model": args.judge_model, "qa_citation": summary,
                   "citation_check": aggregate_cc(rows), "usage_this_run": llm.cost(),
                   "failures": failures}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")

    print(f"\nwrote {out} ({len(rows)} rows) and {out_dir / 'summary.json'}")
    print(json.dumps(summary, indent=2))
    if failures:
        print(f"\n{len(failures)} evaluations failed: {failures}")
        sys.exit(1)


if __name__ == "__main__":
    main()
