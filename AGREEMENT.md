# Inter-rater agreement — CrossSource v0.3

150 items (75 `qa_citation`, 75 `citation_check`), labelled under [LABELING_PROTOCOL.md](LABELING_PROTOCOL.md) v1.0/1.0.1 (the label rules are the same in both). Raw labels: `data/v0.3/labels/rater_a.jsonl`, `rater_b_round1.jsonl`. Numbers: `data/v0.3/labels/agreement_round1.json`. To recompute: `python src/v03_dataset.py agreement --round 1`.

## Who the raters are
- **Rater A**: the label the generator wrote while building the item (Claude Sonnet 5.5 subagent, following §4).
- **Rater B**: a separate Claude Sonnet 5.5 subagent run. It saw only the protocol, its brief, and label-free items in a folder outside the repository. Item ids were replaced with opaque hashes, because draft keys encode build order and so leak the target label. Rater B never saw rater A's labels or reasons.

Both raters are the **same model family**, so these numbers are **model–model agreement, not human inter-rater reliability**. The human check is the adjudication pass ([ADJUDICATION.md](ADJUDICATION.md)).

## Results (round 1, all 150 items)

| Type | n | Percent agreement | Cohen's kappa | Notes |
|---|---|---|---|---|
| `citation_check` | 75 | 98.7% | 0.982 | 4-way label |
| `qa_citation` | 75 | 78.7% (exact chunk set) | 0.835 (chunk level, 375 decisions) | chunk-level agreement 94.1%; mean Jaccard 0.881 |

`citation_check` confusion (rows = rater A, columns = rater B):

| A \ B | supported | right_doc_wrong_passage | wrong_document | unsupported_claim |
|---|---|---|---|---|
| supported | 29 | 0 | 0 | 1 |
| right_doc_wrong_passage | 0 | 15 | 0 | 0 |
| wrong_document | 0 | 0 | 15 | 0 |
| unsupported_claim | 0 | 0 | 0 | 15 |

For `qa_citation`, kappa is computed over binary decisions: each chunk in each item's candidate window counts as one ground-truth / not-ground-truth decision per rater.

**Hamilton replacement (2026-10-20).** The 5th Cir. *Hamilton v. Dallas County* panel opinion (later abrogated en banc) was removed. The 6 Title VII items that used it, 3 as their source and 3 as context distractors, were rebuilt with the same labels on *Rodriguez v. City of Corpus Christi* (5th Cir. 2025). Rater B labelled them blind and agreed with rater A on all 6. The superseded rater B labels are kept in `data/v0.3/labels/superseded_hamilton_rater_b.jsonl`. The table above already includes the rebuilt items.

## What the disagreements show
- **All 16 `qa_citation` disagreements go the same way.** Rater B chose a strict superset of rater A's chunks. Rater A marked one chunk on 74 of 75 items. Rater B marked one chunk on 58, two on 12, three on 4 and four on 1.
  - The extra chunks restate a Must-mention point, or carry half of a sentence that the chunker split.
  - §3.1 rules 2–3 tell the rater to mark both in those cases. So in most of these items rater B applied the protocol as written, and rater A under-marked because it labelled from the chunk it built the item around.
  - Recommended adjudications accept rater B's set on 13 of 16 items and part of it on the other 3.
- **The single `citation_check` disagreement** (`first_amendment_employee-cc-5`) is a wording slip in the claim: it says "the mayor" where the passage names the person, and the mayor's identity sits in a chunk outside the context set.

## Protocol tightening and re-run
The brief asked me to keep the adjudication queue under 40 by tightening the protocol and re-running the raters once *if needed*. Round 1 gives 17 disagreements plus a 10% audit of 13, so **30 items: no re-run was needed and none was done.** The protocol was not changed after labelling began.

A **proposed amendment for v1.1**, not applied: §3.1 should say explicitly that the ground-truth set must include every chunk in the window that alone states a Must-mention point. Rater A should then re-label `qa_citation` with the window shown, not from the build chunk. That would remove the systematic under-marking above.

## Caveats a reader should weigh
1. **The `citation_check` agreement is near ceiling, and that is not evidence the items are hard.**
   - The items are constructed: three of the labels come from controlled substitutions or perturbations (§4).
   - Both raters share a model family.
   - §1.3 of the protocol, which rater B read, states the target label mix (30/15/15/15). Rater B's distribution was 29/15/15/16. Rater B could have used that mix as a prior.
   - A human-labelled sample of these items is the next thing to get before this figure is used as a reliability claim. The v1.1 rater copy should also leave out the target mix.
2. **Rater B ran in two sessions**: 70 items, then 80 after the 10 replacement opinions were fetched. The second session was paused once by the environment's auto-mode classifier at item 11. It resumed with the curator's approval and kept its first 11 labels. Rater B also once read a tool-output overflow file of its own item text; that file held no labels.
3. **`qa_citation` ground truth is rater A's build-time chunk unless adjudicated.** Citation recall in the harness is measured against that set, so until adjudication lands it under-credits citations of restating chunks.
