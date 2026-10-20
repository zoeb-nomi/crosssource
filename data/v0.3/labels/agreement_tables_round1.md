| Type | n | Percent agreement | Cohen's kappa | Notes |
|---|---|---|---|---|
| `citation_check` | 75 | 98.7% | 0.982 | 4-way label |
| `qa_citation` | 75 | 78.7% (exact chunk set) | 0.835 (chunk-level, 375 decisions) | chunk-level agreement 94.1%; mean Jaccard 0.881 |

`citation_check` confusion (rows = rater A, columns = rater B):

| A \ B | supported | right_doc_wrong_passage | wrong_document | unsupported_claim |
|---|---|---|---|---|
| supported | 29 | 0 | 0 | 1 |
| right_doc_wrong_passage | 0 | 15 | 0 | 0 |
| wrong_document | 0 | 0 | 15 | 0 |
| unsupported_claim | 0 | 0 | 0 | 15 |
