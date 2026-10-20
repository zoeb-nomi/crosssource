"""Re-score saved v0.3 sanity-pass outputs against the current (final) labels — no API calls.

Reads   results/v0.3/<model>/raw_results.jsonl   (from run_eval.py --dataset v0.3)
Writes  results/v0.3/<model>/summary_final_labels.json

- qa_citation: citation recall and missing_authority are recomputed against the final
  ground_truth_chunks. Citation precision, faithfulness and relevance are judge verdicts
  that don't depend on the labels, so they carry over unchanged.
- citation_check: accuracy / kappa recomputed against the final label.
- Rows whose item was rebuilt after the run (question or claim text no longer matches the
  current item) can't be re-scored without a new API call, so they are dropped and listed.

Usage:  python src/v03_rescore.py results/v0.3/claude-sonnet-5-5 results/v0.3/gpt-5-mini
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_eval import aggregate_cc, aggregate_qa  # noqa: E402
from v03_dataset import V3, jl_read  # noqa: E402


def rescore(run_dir: Path):
    qa = {it["id"]: it for it in jl_read(V3 / "qa_citation.jsonl")}
    cc = {it["id"]: it for it in jl_read(V3 / "citation_check.jsonl")}
    rows, dropped, changed = [], [], 0
    for r in jl_read(run_dir / "raw_results.jsonl"):
        if r.get("type") == "citation_check":
            it = cc.get(r["id"])
            if not it:
                dropped.append((r["id"], "item no longer exists"))
                continue
            gold = it["label"]
            changed += gold != r["gold"]
            rows.append({**r, "gold": gold, "correct": r["pred"] == gold})
        else:
            it = qa.get(r["id"])
            if not it or it["question"] != r["question"]:
                if (r["id"], "question changed (item rebuilt after the run)") not in dropped:
                    dropped.append((r["id"], "question changed (item rebuilt after the run)"))
                continue
            truth = it["ground_truth_chunks"]
            cited = set(r["citations"])
            recall = sum(t in cited for t in truth) / len(truth)
            changed += truth != r["ground_truth_chunks"]
            rows.append({**r, "ground_truth_chunks": truth, "citation_recall": round(recall, 4),
                         "missing_authority": [t for t in truth if t not in cited]})
    return rows, dropped, changed


def main():
    for d in sys.argv[1:] or ["results/v0.3/claude-sonnet-5-5", "results/v0.3/gpt-5-mini"]:
        run_dir = Path(d)
        old = json.loads((run_dir / "summary.json").read_text())
        rows, dropped, changed = rescore(run_dir)
        # citation_check rows carry the claim only via the item; flag rebuilt cc items by id
        rebuilt_cc = [r["id"] for r in rows if r.get("type") == "citation_check" and r["id"] in REBUILT_CC]
        rows = [r for r in rows if r["id"] not in rebuilt_cc]
        dropped += [(i, "claim/context changed (item rebuilt after the run)") for i in rebuilt_cc]
        configs = [c for c in ("baseline", "strict") if any(r["config"] == c for r in rows)]
        summary = {
            "model": old["model"], "judge_model": old["judge_model"], "rescored_against": "final labels (v0.3 final)",
            "qa_citation": {c: aggregate_qa(rows, c) for c in configs},
            "citation_check": aggregate_cc(rows),
            "dropped_rows": sorted({(i, why) for i, why in dropped}),
            "rows_with_changed_labels": changed,
            "api_calls": 0, "usage_of_original_run": old.get("usage_this_run"),
        }
        (run_dir / "summary_final_labels.json").write_text(json.dumps(summary, indent=2) + "\n")
        qa_s = summary["qa_citation"]
        print(f"{old['model']}: qa n={qa_s['baseline']['items']} precision {qa_s['baseline']['citation_precision']}/{qa_s['strict']['citation_precision']} "
              f"recall {qa_s['baseline']['citation_recall']}/{qa_s['strict']['citation_recall']} | cc n={summary['citation_check']['items']} "
              f"acc {summary['citation_check']['accuracy']} kappa {summary['citation_check']['kappa']} | dropped {summary['dropped_rows']} | label changes {changed}")


# citation_check items rebuilt after the sanity run (cc rows don't store the claim, so they are listed):
# Hamilton -> Rodriguez (title_vii cc-1..5), Najera Aguirre -> Cuevas (qi cc-1..5), rewritten first_amendment cc-5
REBUILT_CC = ({f"title_vii_retaliation-cc-{i}" for i in range(1, 6)} | {f"qi_excessive_force-cc-{i}" for i in range(1, 6)}
              | {"first_amendment_employee-cc-5"})

if __name__ == "__main__":
    main()
