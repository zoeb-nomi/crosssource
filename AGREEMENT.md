# Inter-rater agreement — CrossSource v0.3

150 items (75 `qa_citation`, 75 `citation_check`). The model raters labelled under [LABELING_PROTOCOL.md](LABELING_PROTOCOL.md) v1.0–1.0.2 (same label rules); the adjudication was decided under v1.1. Raw labels: `data/v0.3/labels/rater_a.jsonl`, `rater_b_round1.jsonl`, `adjudicated.jsonl`. Numbers: `agreement_round1.json` (round 1 as measured) and `agreement_final_items.json` (final item set). To recompute: `python src/v03_dataset.py agreement --round 1`.

## Who the raters are
- **Rater A**: the label the generator wrote while building the item (Claude Sonnet 5.5 subagent, following §4).
- **Rater B**: a separate Claude Sonnet 5.5 subagent run. It saw only the protocol, its brief, and label-free items in a folder outside the repository. Item ids were replaced with opaque hashes, because draft keys encode build order and so leak the target label. Rater B never saw rater A's labels or reasons.

Both raters are the **same model family**, so these numbers are **model–model agreement, not human inter-rater reliability**. The human check is the adjudication pass ([ADJUDICATION.md](ADJUDICATION.md)).

## Results — round 1 as measured (all 150 items, model raters A and B)

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

## Third rater — human adjudication (2026-10-20)
The curator adjudicated all 30 queued items (17 disagreements + a seeded 10% audit of 13 agreed items) under protocol v1.1. The decisions are in `data/v0.3/labels/adjudicated.jsonl`.

| | Items | Result |
|---|---|---|
| Adjudicator agreed with the recommended label | **27 / 30** | |
| Resolved by the v1.1 §3.1 amendment | **3 / 30** | `ineffective_assistance-qa-3` → chunks 8, 9, 10; `patent_obviousness-qa-5` → chunks 4, 5, 6 (both add a chunk to the recommendation); `personal_jurisdiction-qa-2` → 10, 11, 13 (confirmed under the amended rule) |
| Audit sample (agreed items) found wrong | **0 / 13** | below the §7.4 threshold (1 in 10), so neither type is re-labelled wholesale |

- On the 16 `qa_citation` disagreements, the final set is **rater B's on 15**. On *Rios* (`personal_jurisdiction-qa-2`) it is rater B's set minus chunk 9. Rater A's build-time single chunk was never the final answer where the two disagreed.
- The single `citation_check` disagreement (`first_amendment_employee-cc-5`) was settled by **rewriting the claim** to name the person the passage names (adjudication decision 4; v1.1 §5 identifier rule). It keeps its built label `supported`, and rater B, re-run blind on the rewritten item, agrees.

**Rebuilds at adjudication.** *Estate of Najera Aguirre* (9th Cir.) was removed: its caption lists plaintiffs by initials, likely minors. The 7 qualified-immunity items that used it, 4 as their source and 3 as context distractors, were rebuilt with the same labels on *Cuevas v. City of Tulare* (9th Cir. 2024). Rater B, blind, agrees on all 7. Superseded rater B labels: `superseded_adjudication_rebuild_rater_b.jsonl`.

## Final item set (after rebuilds; model raters A vs B)

| Type | n | Percent agreement | Cohen's kappa | Notes |
|---|---|---|---|---|
| `citation_check` | 75 | 100% | 1.000 | the only round-1 disagreement was rewritten |
| `qa_citation` | 75 | 78.7% (exact chunk set) | 0.835 (chunk level, 375 decisions) | chunk-level agreement 94.1%; mean Jaccard 0.881 |

Final labels: adjudicated for the 30 queued items (`label_source: "adjudicated"`). For the other 120, rater A = rater B, and the 53 `qa_citation` among them were re-labelled under v1.1: 51 confirmed, 2 gained a chunk (see below).

## What the disagreements show
- **All 16 `qa_citation` disagreements go the same way.** Rater B chose a strict superset of rater A's chunks. Rater A marked one chunk on 74 of 75 items. Rater B marked one chunk on 58, two on 12, three on 4 and four on 1.
  - The extra chunks restate a Must-mention point, or carry half of a sentence that the chunker split.
  - §3.1 rules 2–3 tell the rater to mark both in those cases. So in most of these items rater B applied the protocol as written, and rater A under-marked because it labelled from the chunk it built the item around.
  - Recommended adjudications accept rater B's set on 13 of 16 items and part of it on the other 3.
- **The single `citation_check` disagreement** (`first_amendment_employee-cc-5`) is a wording slip in the claim: it says "the mayor" where the passage names the person, and the mayor's identity sits in a chunk outside the context set.

## Protocol tightening and re-run
The brief asked me to keep the adjudication queue under 40 by tightening the protocol and re-running the raters once *if needed*. Round 1 gave 17 disagreements plus a 10% audit of 13, so **30 items: no rater re-run was needed and none was done.**

The curator then adopted **protocol v1.1** at adjudication:
- §3.1: a chunk qualifies if it alone lets a reader verify any one Must-mention point in full; a rule-only chunk counts only when the point is the rule itself.
- §2: reasoned per curiam opinions are allowed, and precedential status is recorded but is not a selection criterion.
- §5: claims that depend on an identifier shown only outside the passages are excluded, and interleaved footnote text alone is not "garbled".

**v1.1 re-label of the non-queued `qa_citation` items (2026-10-20).** Per the protocol's version rule, the 53 `qa_citation` items outside the queue were re-labelled under v1.1. This was one blind Claude Sonnet 5.5 subagent run, with opaque ids, an isolated folder and no access to earlier labels. Labels: `data/v0.3/labels/relabel_v11.jsonl`. The 67 `citation_check` items outside the queue were not re-labelled, because their rules did not change.

| 53 non-queued `qa_citation` items | Before (v1.0, agreed) | After (v1.1) |
|---|---|---|
| Unchanged | — | **51** |
| Gained a chunk | — | **2** (`contract_interpretation-qa-4` + `cl6320573:11`; `article_iii_standing-qa-4` + `cl11116328:8`) |
| Lost a chunk | — | 0 |
| 1-chunk ground truth | 53 | 51 |
| 2-chunk ground truth | 0 | 2 |

All 75 `qa_citation` items, by ground-truth size: before re-label 59 / 11 / 5 (1 / 2 / 3 chunks); after **57 / 13 / 5**. The 2 changes come from a single rater and were applied without a second rater; each item records `label_source`.

## Caveats a reader should weigh
1. **The `citation_check` agreement is near ceiling, and that is not evidence the items are hard.**
   - The items are constructed: three of the labels come from controlled substitutions or perturbations (§4).
   - Both raters share a model family.
   - §1.3 of the protocol, which rater B read, states the target label mix (30/15/15/15). Rater B's distribution was 29/15/15/16. Rater B could have used that mix as a prior.
   - A human-labelled sample of these items is the next thing to get before this figure is used as a reliability claim. The v1.1 rater copy should also leave out the target mix.
2. **Rater B ran in two sessions**: 70 items, then 80 after the 10 replacement opinions were fetched. The second session was paused once by the environment's auto-mode classifier at item 11. It resumed with the curator's approval and kept its first 11 labels. Rater B also once read a tool-output overflow file of its own item text; that file held no labels.
3. **The v1.1 re-label is a single model rater.** Its 2 changes were not second-rated or human-checked.
4. **The human pass covers 30 of 150 items.** The other 120 rest on model–model agreement.
