# CrossSource v0.1 — Results

Golden set: 25 human-authored questions; each answered and scored under both configurations. Judge validated against blind human labels (see judge_agreement.md).

| Dimension | baseline | strict |
|---|---|---|
| Citation precision | 0.981 | 0.994 |
| Citation recall | 0.760 | 0.760 |
| Faithfulness | 1.000 | 1.000 |
| Answer relevance | 0.980 | 0.960 |

## Citation-failure taxonomy (counts)

| Failure mode | baseline | strict |
|---|---|---|
| missing_authority | 6 | 6 |
| right_doc_wrong_passage | 3 | 1 |

The configurations share one model and differ only in citation-discipline
system-prompt rules; deltas isolate the effect of prompted citation discipline.
