# CrossSource labelling protocol — v0.3

Version 1.0.2 (2026-10-20). Any change after raters start gets a new version number and an entry in the changelog at the bottom; items labelled under an older version are re-labelled, not grandfathered.

This protocol governs every item in `data/v0.3/`. The 25 v0.1 items (`data/golden.jsonl`) were built under different source rules (Caselaw Access Project, pre-2018 landmark cases) and are kept unchanged as the `v0.1-legacy` split. They are not counted toward the 150 and are not re-labelled.

---

## 1. Item types

v0.3 has two types, 75 items each.

### 1.1 `qa_citation` (existing type, unchanged in shape)
A question about one opinion. A correct answer is found in one or more chunks of that opinion. The system under test must answer and cite those chunks.

- **Label** = `ground_truth_chunks`: the set of chunk ids (`doc_id:chunk_id`) that a reader needs in order to verify a correct answer.
- **Reference notes**: "Must mention: …" — the points a correct answer must contain.

### 1.2 `citation_check` (new type)
A claim with a citation already attached, plus the passages the citing system "had available". The task is to say whether the citation is good and, if not, what kind of failure it is. This is exactly the decision the harness's citation-precision judge makes, so this type measures the judge directly.

- **Label** = one of `supported`, `right_doc_wrong_passage`, `wrong_document`, `unsupported_claim` (definitions in §3.2). These are the harness's existing failure-taxonomy labels.

**Why a second type.** The brief allows one new type only if the existing type cannot reach 150 with balance. `qa_citation` can reach 150 items, but it cannot reach *label* balance: every item is answerable by construction, so its only label is a chunk set, and the 4-way taxonomy that the harness reports never appears as a ground-truth label. v0.1's own biggest weakness was that the judge was checked on just 15 verdicts. A 75-item `citation_check` set with a fixed label mix fixes both.

### 1.3 Target counts

| Type | Items | Label mix |
|---|---|---|
| `qa_citation` | 75 | 1 ground-truth chunk: ≥ 45; 2 chunks: ≤ 30 |
| `citation_check` | 75 | `supported` 30 · `right_doc_wrong_passage` 15 · `wrong_document` 15 · `unsupported_claim` 15 |

---

## 2. Source rules

Every v0.3 item comes from opinions that meet **all** of these:

| Rule | Requirement |
|---|---|
| Source | CourtListener REST API v4 (Free Law Project). Opinion text taken from the `plain_text` field, or from `html_with_citations` / `html` with tags removed, in that order of preference — or, when the API quota is exhausted, from the opinion's PDF in CourtListener's public file storage (`storage.courtlistener.com/<local_path>`), accepted only if its SHA-1 matches the `sha1` in the verbatim REST search response. Each document records which source it used (`text_field`). |
| Publication status | `Published` only (CourtListener cluster field `precedential_status`; stored as `publication_status` in `sources.json`). |
| Date | `date_filed` on or after 2018-01-01. |
| Court | A federal court of appeals (`ca1`–`ca11`, `cadc`, `cafc`) or a state court of last resort (the court CourtListener lists as that state's highest court, e.g. `cal`, `ny`, `tex`, `mass`). In Texas and Oklahoma, which have two courts of last resort, use the civil supreme court only. |
| Language | English. |
| Opinion type | Lead / majority / combined opinion. No concurrences, no dissents, no per curiam summary orders. |
| Length | At least 1,500 words of opinion text (enough for ≥ 4 chunks). |
| Precedential status | Not abrogated, overruled or vacated. Every opinion is screened by searching CourtListener for later opinions that cite it and use abrogation / overruling / vacatur language (`src/v03_fetch.py treatment`). Zero hits → `good law` (screen basis, dated). Any hit is read by hand and set to `good law`, `abrogated`, `overruled` or `unknown` with the evidence in `data/v0.3/treatment.json`. `sources.json` carries `precedential_status` for every opinion; the validator rejects items that touch an `abrogated` / `overruled` opinion and, by default, an `unknown` one. This is a screen, not a citator (Shepard's / KeyCite). |

**Spread.**
- At least 40 distinct opinions across the 150 items; no opinion supplies more than 4 items.
- Federal circuit vs state supreme court: each between 40% and 60% of items.
- No single court supplies more than 15% of items.
- Each item carries an `area_of_law` tag (`constitutional`, `criminal`, `civil_procedure`, `contracts`, `torts`, `employment`, `administrative`, `ip`, `other`); no tag above 30%.

**Hard exclusions (whole opinion).**
- Any opinion in which the curator's current employer is a party, amicus or otherwise named.
- Family law, juvenile, adoption and sexual-offence cases; opinions that name or describe a minor or a victim of a sexual offence.
- Sealed or redacted opinions.
- Attorney-discipline opinions about a named individual.

### 2.1 Provenance — required on every item

| Field | Meaning |
|---|---|
| `opinion_id` | CourtListener opinion id |
| `cluster_id` | CourtListener cluster id |
| `url` | `https://www.courtlistener.com` + the cluster's `absolute_url` |
| `case_name`, `court_id`, `date_filed` | from the cluster / docket |
| `passage` | the exact text of the ground-truth chunk (or cited chunk for `citation_check`), byte-for-byte as it appears in `data/v0.3/corpus/<doc_id>.txt` |
| `cited_authority` | the authority the passage relies on, copied **as it appears** in the opinion, including pin cite and parenthetical year (e.g. `Terry v. Ohio, 392 U.S. 1, 30 (1968)`) |

Items are rejected by `src/v03_validate.py` if any field is empty, if `passage` is not an exact substring of the stored opinion text, or if `cited_authority` is not an exact substring of `passage`.

### 2.2 Corpus and chunking
Each accepted opinion is saved to `data/v0.3/corpus/<doc_id>.txt` with `doc_id = cl<opinion_id>` (lowercase, matches the harness's `[a-z0-9_]+` id rule). Text is normalised once — tags stripped, runs of whitespace inside a line collapsed, paragraph breaks kept — and then frozen. Chunking uses the unchanged v0.1 chunker (`src/retrieval.py`, ~350 words). Chunk ids are positional, so neither the normaliser nor the chunker may change after items are written.

Raw API responses are cached under `data/raw/` (gitignored). The corpus files are the frozen, committed derivative.

---

## 3. Label definitions and decision rules

Shared rule for both types: **judge only from the text shown.** Do not use what you know about the case, the law, or the cited authority. If the passage does not say it, it is not there.

### 3.1 `qa_citation` — choosing the ground-truth chunks

You see a question, reference notes, and a **candidate window**: the chunk the item was built from plus up to two chunks either side of it in the same opinion (≤ 5 chunks, shown in order).

Mark a chunk as ground truth if **and only if** it states at least one of the "Must mention" points, such that a reader could verify that point from that chunk alone.

Decision rules:
1. A chunk that only *mentions* the topic, quotes the question's words, or sets up the issue without stating the point is **not** ground truth.
2. If the same point is stated in two chunks, mark **both**.
3. A point split across a chunk boundary (half a sentence in each): mark both chunks.
4. A point stated only in a footnote that the chunker has placed in a chunk: that chunk counts.
5. If you think no chunk in the window states a "Must mention" point, mark none and flag the item `bad_item` (see §5).

### 3.2 `citation_check` — one label per item

You see a CLAIM, the CITED passage, and up to four OTHER passages that the citing system had available. Each passage is labelled with its `doc_id:chunk_id`; passages with the same `doc_id` come from the same opinion.

Work through these questions **in order** and stop at the first "yes":

| Step | Question | If yes → label |
|---|---|---|
| 1 | Does the CITED passage, read alone, state everything the claim asserts? | `supported` |
| 2 | Does an OTHER passage from the **same opinion** state everything the claim asserts? | `right_doc_wrong_passage` |
| 3 | Does an OTHER passage from a **different opinion** state everything the claim asserts? | `wrong_document` |
| 4 | None of the above. | `unsupported_claim` |

"States everything the claim asserts" means every factual and legal element of the claim is in that one passage. Paraphrase is fine; added substance is not.

Edge cases:
- **Partial support.** If the cited passage supports most of the claim but not all of it (e.g. the claim says "held X and remanded" and the passage only says "held X"), it is **not** `supported`. Carry on down the steps.
- **Overstatement.** A claim that turns "may" into "must", "some" into "all", a plurality into a holding, or dicta into a holding is not supported by a passage that says the weaker thing.
- **The court quoting someone else.** If the passage says the court *rejected* or is merely *reporting* a party's argument, a claim that the court *adopted* that argument is unsupported by it.
- **Cited authority.** A claim about what the *cited authority* held is supported only if the passage itself says what that authority held. The passage citing a case is not support for a claim about that case's holding.
- **Two passages together.** If the claim is supported only by combining two passages, no single passage supports it → follow the steps as written (usually `unsupported_claim`). Do not invent a combined label.
- **Supported by both cited and another passage.** Step 1 wins: `supported`.
- **Supported by a same-opinion passage and a different-opinion passage** (cited fails): step 2 wins: `right_doc_wrong_passage`.

---

## 4. How items are built (generator instructions)

The generator drafts items from cached opinions; raters never see its working.

**`qa_citation`.** Pick a chunk that states a legal rule, test, holding or reasoning step and that contains at least one cited authority. Write a question that names the case and the court (so it is anchored to this opinion) and is answerable from that chunk. Write "Must mention" notes (1–3 points). Record the chunk (and a second chunk only if the point genuinely spans two). Do not copy a full sentence of the passage into the question.

**`citation_check`.** Build a context set of 5 passages: the cited passage, at least one other passage from the same opinion, and at least one passage from a different v0.3 opinion on a related topic. Then write the claim for the target label:
- `supported` — a faithful paraphrase of something the cited passage states.
- `right_doc_wrong_passage` — a faithful paraphrase of a *different* same-opinion passage in the context set; cite a same-opinion passage that is on a nearby topic but does not state it.
- `wrong_document` — a faithful paraphrase of the different-opinion passage; cite a passage from the first opinion.
- `unsupported_claim` — start from a supported claim and change one thing a careful reader would catch: reverse the outcome, swap the standard (e.g. "clear error" → "de novo"), overstate scope, misattribute a party's argument to the court, or assert the cited authority held something the passage doesn't say. The changed claim must not be supported by any passage in the context set.

Claims are one or two sentences and must read like something a RAG system would actually write. Context passage order is shuffled.

---

## 5. Inclusion and exclusion (per item)

Include an item only if:
- it meets every §2 rule and the §2.1 provenance check passes;
- a rater can decide its label from the text shown, without outside knowledge;
- (qa) the question is answerable from the passage and names the case;
- (citation_check) the claim is one or two sentences and the context set has ≥ 1 same-opinion and ≥ 1 different-opinion passage.

Exclude (or have the rater flag `bad_item`) if:
- the passage is boilerplate (standard of review, jurisdiction statement, procedural history only);
- the passage is not the court's own text: a staff-prepared summary, syllabus or headnote, a caption, or a counsel list;
- the passage is mainly a block quote of a statute, regulation, contract or jury instruction;
- the question or claim can be answered from general legal knowledge without the passage *and* the passage does not add anything specific;
- the text is garbled (OCR errors, broken footnote markers) in a way that changes meaning;
- the item would require any personal information beyond party names already in the case caption.

A rater who flags `bad_item` still gives a best-effort label, plus a one-line reason. `bad_item` flags go to adjudication.

---

## 6. Rater instructions (for a law student or an independent model)

1. You will get one item at a time. You will **not** see anyone else's label, the generator's notes, or which label the item was built to have.
2. Read the protocol §3 for that item's type. Use only the text in front of you.
3. **qa_citation:** read the question and the "Must mention" notes. Read every chunk in the window. List the chunk ids that state at least one "Must mention" point (§3.1). Give one sentence saying which point each chosen chunk states.
4. **citation_check:** read the claim. Work through steps 1–4 of §3.2 in order. Give the label and one sentence naming the passage (by id) and the words that decided it — or, for `unsupported_claim`, the element of the claim that no passage states.
5. If the item is broken (§5), add `bad_item: <reason>` and still give your best label.
6. Do not look anything up. Do not go back and change earlier answers after seeing later items.

Output per item: `{"id", "label", "reason", "bad_item": null | "<reason>"}` where `label` is a list of chunk ids (qa) or one of the four strings (citation_check).

---

## 7. Agreement and adjudication

**Raters.** Rater A = the label the generator wrote. Rater B = an independent labeller who sees only this protocol and the unlabelled item. In this release both raters are separate runs of the same model family (Claude Sonnet), so the reported numbers are model–model agreement, not human inter-rater reliability; the human adjudication pass is the human check.

**Agreement measures.**
- `citation_check`: percent agreement and Cohen's kappa on the 4-way label.
- `qa_citation`: (a) percent of items where both raters chose the identical chunk set; (b) Cohen's kappa on the binary chunk-level decisions (every candidate-window chunk × item = one yes/no decision per rater); (c) mean Jaccard overlap of the chosen sets.

**Adjudication rule.**
1. Every disagreement, every `bad_item` flag, and a seeded random 10% of agreed items go to `ADJUDICATION.md`.
2. The adjudicator (the dataset curator) reads the item and both reasons, applies §3 as written, and records a final label. The adjudicator may pick A, B, or a third label.
3. If the protocol does not decide the case, the item is **dropped** (not forced), and a protocol amendment is drafted for the next version.
4. If more than 1 in 10 of the audited agreed items is wrong, the whole type is re-labelled after the protocol is tightened.
5. Final labels are the adjudicated label where one exists, otherwise the agreed label.

---

## Changelog
- **1.0 (2026-10-19)** — first version.
- **1.0.1 (2026-10-20)** — source rule only: SHA-1-verified CourtListener storage PDFs allowed as a text source; §5 excludes staff summaries/syllabi. Label definitions unchanged, so no re-labelling.
- **1.0.2 (2026-10-20)** — source rule only: precedential-status screen and `precedential_status` field (added after a 5th Cir. panel opinion later abrogated en banc slipped in). Label definitions unchanged.
