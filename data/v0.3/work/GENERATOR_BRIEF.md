# Generator brief — CrossSource v0.3 (rater A)

You draft the v0.3 items. Read `LABELING_PROTOCOL.md` in full first (§1, §3, §4, §5 especially) — it is the rulebook; this brief only adds logistics. Everything you need is on disk; never use outside knowledge of these cases or the law.

## Inputs
`data/v0.3/work/packets/<topic_key>.json` — one file per topic (15). Each lists 3 opinions with every chunk: `{"id": "cl123:4", "has_case_citation": bool, "text": ...}`.

Work **one topic at a time**: read the packet, write that topic's drafts file, then move on. Do not read other topics' packets while drafting a topic.

## Output per topic: `data/v0.3/work/drafts/<topic_key>.jsonl` — exactly 10 lines

**5 × `qa_citation`** (§1.1, §4):
```
{"draft_key": "<topic_key>-qa-1", "type": "qa_citation", "topic_key": "...", "question": "...", "reference_notes": "Must mention: ...", "ground_truth_chunks": ["cl123:4"], "cited_authority": "<verbatim>", "rater_a_reason": "<which chunk states which Must-mention point>"}
```
**5 × `citation_check`** with labels exactly: 2 `supported`, 1 `right_doc_wrong_passage`, 1 `wrong_document`, 1 `unsupported_claim`:
```
{"draft_key": "<topic_key>-cc-1", "type": "citation_check", "topic_key": "...", "claim": "...", "cited_chunk": "cl123:7", "context_chunks": ["cl123:7", "cl123:9", "cl123:2", "cl456:5", "cl789:3"], "label": "supported", "cited_authority": "<verbatim>", "rater_a_reason": "<the §3.2 step that decides it and the passage id + words>", "construction_note": "<how you built it; for unsupported_claim, exactly what you changed>"}
```

## Hard rules (the validator rejects violations)
- Chunk ids must exist in the packet, copied exactly.
- `cited_authority` = a case citation copied **character-for-character** from the ground-truth chunk (qa; the first one if two) or from the `cited_chunk` (cc), e.g. `Pearson v. Callahan, 555 U.S. 223, 236` — include the case name only if it appears contiguously with the citation in the text. Pick only chunks with `has_case_citation: true` for these roles. Copy, don't retype from memory: watch line breaks, curly quotes, section signs, "Id." forms (avoid Id. — pick a full citation).
- qa: question names the case (short name is fine) and the court; 1–3 Must-mention points; ground truth is 1 chunk, or 2 only if a point genuinely spans them. Across all 75 qa items at most 30 may have 2 chunks — aim for ≤ 2 per topic.
- cc: `context_chunks` has exactly 5 ids, includes `cited_chunk`, ≥ 1 other chunk from the cited opinion, ≥ 1 chunk from a different opinion in this topic. For `wrong_document`, the supporting passage is from a different opinion and the cited chunk is from the first; for `right_doc_wrong_passage`, the supporting passage is another chunk of the cited opinion and the cited chunk does not state the claim. For `unsupported_claim`, make ONE change a careful reader would catch (§4) and make sure no passage in the context set supports the changed claim. For `supported`, the claim must not add anything the cited passage doesn't state.
- Spread: per topic, no opinion may supply more than 4 of the 10 items (an item belongs to the opinion of its ground-truth chunk / cited chunk). Use all 3 opinions.
- Never use text the court did not write: staff-prepared SUMMARY / syllabus / headnotes (e.g. the Ninth Circuit's "SUMMARY" block, which says it is not part of the opinion), captions, counsel lists.
- Skip boilerplate chunks (standard of review, jurisdiction, procedural history, caption/counsel lists) and chunks that are mostly a block quote of a statute or contract (§5).
- A claim must be verifiable from the shown passages alone: no name, title, role or date that appears only outside the context set (protocol v1.1 §5).
- Claims and questions in plain professional English; don't copy a full sentence of the passage into a question or claim.

## Self-check before moving on
After writing each file, run:
`.venv/bin/python -c "import json,sys; rows=[json.loads(l) for l in open(sys.argv[1])]; print(len(rows), [r['label'] for r in rows if r['type']=='citation_check'])" data/v0.3/work/drafts/<topic_key>.jsonl`
and confirm 10 rows and the label mix. When all 15 are done, report a one-line count per topic and anything you couldn't satisfy — no item text.
