"""Generate results/results.md (table) and results/scores.png (chart)
from results/summary.json.

Usage:  python src/report.py
"""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS = Path(__file__).resolve().parent.parent / "results"
DIMS = [
    ("citation_precision", "Citation\nprecision"),
    ("citation_recall", "Citation\nrecall"),
    ("faithfulness", "Faithfulness"),
    ("relevance", "Answer\nrelevance"),
]
# validated categorical palette (colorblind-safe, checked with a CVD validator)
COLORS = {"baseline": "#2a78d6", "strict": "#eb6834"}
INK, MUTED, GRID = "#1C2126", "#5B6470", "#E3E2DC"


def make_table(summary):
    lines = [
        "# CrossSource v0.1 — Results",
        "",
        f"Golden set: {summary['baseline']['items']} human-authored questions; "
        "each answered and scored under both configurations. "
        "Judge validated against blind human labels (see judge_agreement.md).",
        "",
        "| Dimension | baseline | strict |",
        "|---|---|---|",
    ]
    for key, label in DIMS:
        lines.append(f"| {label.replace(chr(10), ' ')} | "
                     f"{summary['baseline'][key]:.3f} | {summary['strict'][key]:.3f} |")
    lines += ["", "## Citation-failure taxonomy (counts)", "", "| Failure mode | baseline | strict |", "|---|---|---|"]
    all_labels = sorted(set(summary["baseline"]["failure_labels"]) | set(summary["strict"]["failure_labels"]))
    for lab in all_labels:
        lines.append(f"| {lab} | {summary['baseline']['failure_labels'].get(lab, 0)} "
                     f"| {summary['strict']['failure_labels'].get(lab, 0)} |")
    lines += [
        "",
        "The configurations share one model and differ only in citation-discipline",
        "system-prompt rules; deltas isolate the effect of prompted citation discipline.",
    ]
    (RESULTS / "results.md").write_text("\n".join(lines) + "\n")


def make_chart(summary):
    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=150)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    width, x = 0.36, range(len(DIMS))
    for i, config in enumerate(("baseline", "strict")):
        vals = [summary[config][k] for k, _ in DIMS]
        offset = (i - 0.5) * (width + 0.04)
        bars = ax.bar([p + offset for p in x], vals, width, label=config,
                      color=COLORS[config], edgecolor="white", linewidth=1)
        for bar, v in zip(bars, vals):
            ax.text(bar.get_x() + bar.get_width() / 2, v + 0.015, f"{v:.2f}",
                    ha="center", va="bottom", fontsize=8.5, color=MUTED)

    ax.set_xticks(list(x))
    ax.set_xticklabels([label for _, label in DIMS], fontsize=9.5, color=INK)
    ax.set_ylim(0, 1.1)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.tick_params(colors=MUTED, length=0)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(GRID)

    ax.set_title("Citation-discipline prompting: eval scores by configuration",
                 fontsize=11, color=INK, pad=14, loc="left")
    ax.legend(frameon=False, fontsize=9.5, loc="lower right")
    fig.tight_layout()
    fig.savefig(RESULTS / "scores.png", bbox_inches="tight")
    print("wrote results/scores.png and results/results.md")


if __name__ == "__main__":
    summary = json.loads((RESULTS / "summary.json").read_text())
    make_table(summary)
    make_chart(summary)
