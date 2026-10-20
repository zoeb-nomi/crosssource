# Rater brief — CrossSource v0.3 (rater B, independent)

You label items using **only** `LABELING_PROTOCOL.md` (read it in full, especially §3, §5, §6) and the item text in front of you. You have not seen, and must not look for, anyone else's labels.

**Forbidden files** (do not open, list, grep or read in any way): `data/v0.3/qa_citation.jsonl`, `data/v0.3/citation_check.jsonl`, anything under `data/v0.3/labels/` other than your own output file, anything under `data/v0.3/work/drafts/`, `data/v0.3/work/construction_notes.jsonl`, `data/v0.3/work/packets/`, `data/v0.3/work/GENERATOR_BRIEF.md`, and `data/v0.3/corpus/`. Your only inputs are the protocol and `data/v0.3/work/rater_input/batch_*.jsonl`.

## Per item
- `qa_citation`: question, reference notes, and the candidate window (≤ 5 chunks). Label = list of chunk ids that state at least one "Must mention" point (§3.1). May be empty only if you also flag `bad_item`.
- `citation_check`: claim, the cited passage, and the other passages. Label = one of `supported`, `right_doc_wrong_passage`, `wrong_document`, `unsupported_claim`, decided by walking §3.2 steps 1→4 in order. Passages with the same `cl<number>` prefix are from the same opinion.

## Output
Append one JSON line per item to `data/v0.3/labels/<OUTFILE>`:
`{"id": "...", "label": [...] or "...", "reason": "<one sentence: the deciding passage id and words, or the missing element>", "bad_item": null or "<reason>"}`

Work batch by batch in file order; within a batch, label every item before moving on; never revise an earlier answer after seeing later items (§6.6). After each batch, check with Bash that your output has one line per item so far and that every label is valid.

When done, report only: number of items labelled, the label distribution for citation_check, the number of `bad_item` flags. No item text.
