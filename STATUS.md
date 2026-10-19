# STATUS — what exists before v0.3 (snapshot 2026-10-19, `main` @ 2a09f4b)

Written before any v0.3 change, so it describes v0.1 as published (Zenodo concept DOI 10.5281/zenodo.21969577).

## What the repo is
An eval harness that measures citation-level reliability of a RAG system on public US court opinions. One model answers questions over BM25-retrieved chunks with mandatory inline `[doc_id:chunk_id]` citations, under two prompt configs (`baseline`, `strict`); an LLM judge scores the answers.

## Dataset
| Thing | Where | Shape |
|---|---|---|
| Golden set | `data/golden.jsonl` | **25 items**, one task type. Fields: `id` (g01–g25), `question`, `reference_notes` ("Must mention: …"), `ground_truth_chunks` (list of `doc_id:chunk_id`). No label field, no provenance per item. |
| Corpus | `data/corpus/*.txt` | **22 opinions** (16 SCOTUS, 2 federal circuit, 4 state high court), 1803–1990s landmark cases. One plain-text file per opinion; `doc_id` = file stem (`[a-z0-9_]+`). |
| Provenance | `data/sources.json` | Per *document*: case name, reporter citation, court, date, CAP URL, CAP id, opinion type, char count. Source is the **Caselaw Access Project** static files, not CourtListener — the README says CourtListener now needs auth for opinion text, so the fetcher used CAP. |

Chunking (`src/retrieval.py`) packs paragraphs into ~350-word chunks; chunk ids are positional per document, so the chunker must not change once items reference chunk ids. Adding new documents does not move existing ids.

## Task types
Only one: **`qa_citation`** — a question answerable from one or more ground-truth chunks, with reference notes listing what a correct answer must say. The four-label failure taxonomy (`right_doc_wrong_passage`, `wrong_document`, `unsupported_claim`, `missing_authority`) is a *scoring output*, not an item type.

## How the harness scores (`run_eval.py`, `src/evaluate.py`)
For each item × config: retrieve top-5 → generate → score four dimensions:
- **Citation precision** — LLM judge checks each (claim, cited chunk) pair against the chunk text, given the other retrieved chunks; failures get one of three taxonomy labels.
- **Citation recall** — programmatic: fraction of `ground_truth_chunks` cited; misses logged as `missing_authority`.
- **Faithfulness** — RAGAS-style claim support against retrieved context.
- **Answer relevance** — 0 / 0.5 / 1.

Results stream to `results/raw_results.jsonl` (resumable), aggregate to `results/summary.json`; `src/report.py` builds `results/results.md` + `scores.png`. Generator and judge default to `claude-opus-4-8`; **Anthropic only** — there is no OpenAI path. Full run ≈ 450 calls, ≈ $10.

## Validation that exists
`src/judge_check.py` + `results/judge_agreement.md`: 15 judge verdicts labelled blind by one human (non-lawyer) → 100% agreement. Percent agreement only; no kappa; no inter-rater agreement on the golden set itself.

## Gaps against the v0.3 goal
1. **One task type**, and it has no categorical label, so Cohen's kappa has nothing natural to run on.
2. **Source rules differ**: v0.1 is CAP, pre-2018, mostly SCOTUS. The v0.3 rules (CourtListener, 2018+, federal circuits + state supreme courts) exclude all 25 existing items and all 22 corpus documents.
3. **No per-item provenance** (opinion id, URL, exact passage, cited authority as it appears).
4. **Methodology claim in README**: "every question and note is human-written — a synthetic answer key grading a synthetic student is circular." A model-generated v0.3 set contradicts that sentence; it must be scoped to v0.1 and the new method described honestly.
5. **No OpenAI support** for the two-model sanity pass.
6. `.gitignore` has no `data/raw/`.
7. README byline names the author's current employer. Not touched by v0.3; noted only because of the "nothing from my employer" rule — no employer material is in the repo.
