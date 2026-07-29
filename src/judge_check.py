"""M5: validate the LLM judge against human labels.

The eval harness (M4) uses an LLM judge for citation precision. Trusting an
unvalidated judge is the classic LLM-as-judge mistake (Zheng et al., 2023),
so we sample its judgments, have a human label the same (claim, cited
passage) pairs blind, and report human-judge agreement.

Sampling is stratified: every judgment the judge marked unsupported, plus a
seeded random draw of supported ones, up to SAMPLE_N total. Labeling only
easy positives would inflate agreement.

Usage:
  python src/judge_check.py sample            # writes results/judge_sample.json
  python src/judge_check.py score labels.json # writes results/judge_agreement.md
"""

import json
import random
import sys
from pathlib import Path

from retrieval import Retriever

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
SAMPLE_N = 15
SEED = 42


def load_judgments():
    rows = [json.loads(ln) for ln in (RESULTS / "raw_results.jsonl").read_text().splitlines() if ln.strip()]
    out = []
    for r in rows:
        for i, j in enumerate(r["citation_judgments"]):
            out.append({
                "sid": f"{r['id']}/{r['config']}/c{i}",
                "item": r["id"], "config": r["config"],
                "claim": j["claim"], "citation": j["citation"],
                "judge_supported": j["supported"], "judge_label": j["failure_label"],
            })
    return out


def sample():
    judgments = load_judgments()
    unsupported = [j for j in judgments if not j["judge_supported"]]
    supported = [j for j in judgments if j["judge_supported"]]
    rng = random.Random(SEED)
    picked = unsupported[:SAMPLE_N] + rng.sample(supported, max(0, SAMPLE_N - len(unsupported)))
    rng.shuffle(picked)

    retriever = Retriever()
    for j in picked:
        chunk = retriever.get(j["citation"])
        j["passage"] = chunk["text"] if chunk else "(chunk not found)"

    (RESULTS / "judge_sample.json").write_text(json.dumps(picked, indent=1, ensure_ascii=False) + "\n")
    print(f"sampled {len(picked)} judgments ({len(unsupported[:SAMPLE_N])} judge-unsupported, "
          f"{len(picked) - len(unsupported[:SAMPLE_N])} judge-supported) -> results/judge_sample.json")


def score(labels_path):
    sample_by_sid = {j["sid"]: j for j in json.loads((RESULTS / "judge_sample.json").read_text())}
    labels = json.loads(Path(labels_path).read_text())
    joined = []
    for lab in labels:
        j = sample_by_sid.get(lab["sid"])
        if not j:
            sys.exit(f"unknown sid in labels: {lab['sid']}")
        joined.append({**j, "human_supported": bool(lab["supported"]), "human_comment": lab.get("comment", "")})
    if len(joined) < len(sample_by_sid):
        missing = set(sample_by_sid) - {x["sid"] for x in joined}
        sys.exit(f"labels missing for: {sorted(missing)}")

    agree = [x for x in joined if x["human_supported"] == x["judge_supported"]]
    disagree = [x for x in joined if x["human_supported"] != x["judge_supported"]]
    pct = len(agree) / len(joined)

    sup = [x for x in joined if x["judge_supported"]]
    unsup = [x for x in joined if not x["judge_supported"]]
    sup_agree = sum(1 for x in sup if x["human_supported"]) / len(sup) if sup else float("nan")
    unsup_agree = sum(1 for x in unsup if not x["human_supported"]) / len(unsup) if unsup else float("nan")

    lines = [
        "# Judge validation (M5)",
        "",
        f"Human-labeled sample: **{len(joined)}** citation-precision judgments "
        f"({len(unsup)} judge-unsupported, {len(sup)} judge-supported; stratified, seed {SEED}).",
        "",
        f"## Human-judge agreement: **{pct:.0%}** ({len(agree)}/{len(joined)})",
        "",
        f"- On judgments the judge marked *supported*: human agreed {sup_agree:.0%}",
        f"- On judgments the judge marked *unsupported*: human agreed {unsup_agree:.0%}",
        "",
    ]
    if disagree:
        lines.append("## Disagreements")
        lines.append("")
        for x in disagree:
            lines.append(f"- `{x['sid']}` ({x['citation']}): judge said "
                         f"{'supported' if x['judge_supported'] else 'unsupported'}, human said the opposite."
                         + (f" Human note: {x['human_comment']}" if x["human_comment"] else ""))
        lines.append("")
    else:
        lines.append("No disagreements in this sample.")
        lines.append("")
    lines.append("Labels were collected blind (the human never saw the judge's verdict). "
                 "Human labeler is a non-lawyer; see README limitations.")

    (RESULTS / "judge_agreement.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    print("\nwrote results/judge_agreement.md")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "sample":
        sample()
    elif len(sys.argv) > 2 and sys.argv[1] == "score":
        score(sys.argv[2])
    else:
        sys.exit(__doc__)
