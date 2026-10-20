# CrossSource
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21969577.svg)](https://doi.org/10.5281/zenodo.21969577)

**An evaluation harness for RAG answer quality and citation accuracy on public case law.**

By [Zoeb Nomi](https://www.zoebnomi.com) — AI Product Manager at Instead, working on LLM evaluation and RAG output quality. More public evaluation work at [zoebnomi.com](https://www.zoebnomi.com).

Legal AI is a major LLM category whose most famous trust failure is citation hallucination — lawyers have been sanctioned for filing AI-fabricated citations (*Mata v. Avianca*), and academic work (Stanford RegLab, "Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools," Magesh et al., 2024) found even dedicated legal RAG tools hallucinate at meaningful rates. CrossSource is an open, reproducible harness for measuring citation-level reliability of a RAG system on public court opinions.

This project is an independent implementation of published RAG-evaluation methods, applied to a domain where citation errors carry professional consequences.

## Headline results (v0.1)

**Human–judge agreement: 100% (15/15)** on a blind, stratified sample of the LLM judge's citation-precision verdicts — the number that determines whether any of the other numbers can be trusted ([details](results/judge_agreement.md)).

![Eval scores by configuration](results/scores.png)

| Dimension | baseline | strict |
|---|---|---|
| Citation precision | 0.981 | **0.994** |
| Citation recall | 0.760 | 0.760 |
| Faithfulness | 1.000 | 1.000 |
| Answer relevance | 0.980 | 0.960 |

| Citation-failure taxonomy | baseline | strict |
|---|---|---|
| `right_doc_wrong_passage` | 3 | 1 |
| `missing_authority` | 6 | 6 |
| `wrong_document` | 0 | 0 |
| `unsupported_claim` | 0 | 0 |

**What the numbers say.** Both configurations share one model (`claude-opus-4-8`) and differ only in system-prompt citation-discipline rules, so deltas isolate the effect of prompted citation discipline. Three findings:

1. **Citation-discipline prompting works at the margin**: it cut right-document-wrong-passage citations 3→1 (precision 0.981→0.994). Example from the run: asked about *Erie*'s rule for diversity cases, the baseline attached a claim about Pennsylvania common law to chunk `erie_v_tompkins:0` when the supporting text is in `erie_v_tompkins:1` — a citation a reader following it would find wanting.
2. **Neither configuration fabricated**: faithfulness is 1.000 and `unsupported_claim`/`wrong_document` are zero. On a 22-document corpus with clean retrieval, failure lives in *where citations point*, not invented law.
3. **Recall is capped by retrieval, not generation**: both configurations scored 0.760 because on 6 of 25 questions BM25 never surfaced the ground-truth chunk (`missing_authority`), so neither could cite it. Improving the reader can't fix what the retriever never showed it.

## v0.3 dataset — final (2026-10-20)

**150 items** over **45 published US appellate opinions from 2018–2026** (27 federal circuit, 18 state supreme court, 15 legal topics), pulled from CourtListener (Free Law Project). Every item carries provenance: opinion id, URL, the exact passage, and the cited authority as it appears in the opinion. Labels are final: 30 items adjudicated by the curator, the other 120 agreed by two independent model raters.

| Type | Items | Labels |
|---|---|---|
| `qa_citation`: question over one opinion, answer must cite the supporting chunk(s) | 75 | ground-truth chunk set |
| `citation_check`: a claim with a citation attached; is the citation good, and if not, what kind of failure? | 75 | `supported` 30 · `right_doc_wrong_passage` 15 · `wrong_document` 15 · `unsupported_claim` 15 |

- **Protocol:** [LABELING_PROTOCOL.md](LABELING_PROTOCOL.md) **v1.1** covers source rules, label definitions with decision rules and edge cases, rater instructions and the adjudication rule. v1.1 amendments came from adjudication; see the changelog.
- **Agreement:** [AGREEMENT.md](AGREEMENT.md).
  - **Round 1, two blind model raters** (Claude Sonnet 5.5): 98.7% on `citation_check` (κ = 0.98) and 78.7% exact-set on `qa_citation` (chunk-level κ = 0.84).
  - **Human adjudication (third rater):** the adjudicator agreed with the recommended label on **27 of 30** items, resolved 3 via the v1.1 §3.1 amendment, and found **0 of 13** audited agreed items wrong.
  - These are model–model figures plus a 30-item human pass, not full human inter-rater reliability; see the caveats in AGREEMENT.md.
- **Adjudication:** [ADJUDICATION.md](ADJUDICATION.md) covers the 17 disagreements and a 10% audit, each with both labels, reasons, the recommendation and the final decision. Decisions are in `data/v0.3/labels/adjudicated.jsonl` and applied by `src/v03_dataset.py apply-adjudication`. Each item records `label_source` (`adjudicated` or agreed).
- **Data:** `data/v0.3/qa_citation.jsonl`, `data/v0.3/citation_check.jsonl`, `data/v0.3/corpus/` (normalised opinion text), `data/v0.3/sources.json` (per-opinion provenance, including text source), `data/v0.3/labels/`.
- **Rebuild:** `src/v03_fetch.py` (search and fetch; needs `COURTLISTENER_API_TOKEN`), then `src/v03_corpus.py`, then `src/v03_dataset.py` (packets, assemble, validate, rater input, agreement, adjudication). Raw API responses are cached in `data/raw/`, which is gitignored. 33 opinions come from the REST API; 12 come from CourtListener storage PDFs, SHA-1-verified against the search response. Opinions removed during curation, with reasons, are in `data/v0.3/exclusions.json`. Each opinion's later treatment is recorded in `sources.json` as `precedential_status` (good law / abrogated / overruled / unknown), with its basis and date; it is recorded, not used for selection (protocol v1.1 §2).
- **Method note:** unlike v0.1, v0.3 items were **drafted by a model** following the protocol, labelled independently by a second blind model run, and then human-adjudicated (disagreements plus an audit sample). The v0.1 statement that every question is human-written applies to v0.1 only.

### v0.3 harness sanity pass (30-item seeded sample, pipeline check only)

```bash
.venv/bin/python run_eval.py --dataset v0.3 --model claude-sonnet-5-5 --judge-model claude-sonnet-5-5 --sample 30
.venv/bin/python run_eval.py --dataset v0.3 --model gpt-5-mini --judge-model claude-sonnet-5-5 --sample 30
```

| Model | qa citation precision (baseline / strict) | qa citation recall | `citation_check` accuracy (κ) | API cost |
|---|---|---|---|---|
| `claude-sonnet-5-5` | 0.915 / 0.916 | 0.70 | 1.00 (1.00) | $3.31 |
| `gpt-5-mini` (judge `claude-sonnet-5-5`) | 0.744 / 0.841 | 0.70 | 0.93 (0.90) | $0.10 + $1.42 judge |

n = 15 per type: these numbers confirm the pipeline runs end to end, not a model comparison. They were run before adjudication and before the Najera Aguirre and cc-5 rebuilds, so they are not re-scored on the final labels. Summaries are in `results/v0.3/<model>/summary.json`.

## Method (v0.1)

- **Corpus**: 22 famous, public-domain US court opinions (16 Supreme Court, 2 federal circuit, 4 state high court) spanning constitutional law, contracts, torts, employment, civil procedure, and consumer protection. Text from the [Caselaw Access Project](https://case.law) (Harvard Law School Library); every file's provenance is in [`data/sources.json`](data/sources.json). Deliberately small and deliberately BM25-retrieved — the eval harness is the artifact, and a fancier RAG would bury the point.
- **Pipeline**: ~350-word chunks carrying `doc_id:chunk_id`, BM25 top-5 ([`src/retrieval.py`](src/retrieval.py)); a model answers with mandatory inline `[doc_id:chunk_id]` citations under two configurations — *baseline* (citation format only) vs *strict* (explicit citation-discipline rules) ([`src/generate.py`](src/generate.py)).
- **Golden set (v0.1)**: 25 human-authored questions with ground-truth supporting chunks and reference notes ([`data/golden.jsonl`](data/golden.jsonl)). Candidate passages were machine-scouted and verbatim-verified, but every question and note is human-written — a synthetic answer key grading a synthetic student is circular.
- **Scoring** ([`src/evaluate.py`](src/evaluate.py)): citation precision (LLM judge verifies each citation against the cited chunk's text, with a failure taxonomy), citation recall (programmatic, against ground truth), faithfulness in the style of RAGAS (Es et al., 2023), and answer relevance. LLM-as-judge follows Zheng et al. (2023) — including taking its caveats seriously:
- **Judge validation** ([`src/judge_check.py`](src/judge_check.py)): a stratified sample of judge verdicts (every "unsupported" + random "supported") labeled blind by a human, reported as percent agreement. Trusting an unvalidated judge is the failure mode this project exists to avoid. The blind labeling also caught a real harness bug — see Limitations.

## Run it

```bash
git clone <this repo> && cd crosssource
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env   # add your Anthropic API key
.venv/bin/python run_eval.py          # full eval (resumable: --resume)
.venv/bin/python src/report.py        # regenerate results table + chart
```

`run_eval.py` writes per-item results incrementally to `results/raw_results.jsonl` (interruption-safe) and aggregates to `results/summary.json`. A full run makes ~450 API calls (≈$10 at Opus pricing; set `CROSSSOURCE_MODEL` / `CROSSSOURCE_JUDGE_MODEL` to use cheaper models). To rebuild the corpus from source: `python src/fetch_corpus.py && python src/corpus_stats.py`.

## Limitations

- **n=25.** Every aggregate carries wide error bars; treat deltas as directional, not significant.
- **The golden set and judge labels were authored by a non-lawyer** (against famous, extensively documented holdings, verified against the opinion text — but a law-trained annotator, as in Magesh et al., could disagree at the margin).
- **Judge and generator share a model family**, a known self-preference bias (Zheng et al.). The human agreement check is the mitigation, not a cure — 15 labels is a spot-check, not a certification.
- **Human labeling caught a harness bug**: consecutive citations (`[a:1], [a:2]`) produced punctuation-only claim spans, which the judge scored as failures. All three original `unsupported_claim` counts were this artifact; affected items were re-scored after the fix. Kept here because it's the strongest argument in the repo for validating your judge with human eyes.
- **Retrieval is the recall ceiling** (BM25, k=5, no reranking) — by design, but it means citation recall partly measures the retriever.
- **v0.1 corpus** uses CAP static files; v0.3 uses CourtListener (authenticated REST API v4, plus SHA-1-verified storage PDFs).
- **v0.3 labels are model-drafted and model-checked**, human-adjudicated only on the 30-item queue; the `citation_check` agreement is near ceiling, likely partly because items are constructed and raters share a model family (see AGREEMENT.md).

## v0.2 ideas

Retrieval ablations (k, hybrid/rerank) to lift the recall ceiling; a second judge model family to measure cross-model agreement; law-trained annotation of a golden-set sample; more items per case; per-question difficulty tiers.

## References

- Magesh, V., et al. (2024). *Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools.* Stanford RegLab / HAI.
- Es, S., et al. (2023). *RAGAS: Automated Evaluation of Retrieval Augmented Generation.*
- Zheng, L., et al. (2023). *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena.*
- Robertson, S., & Zaragoza, H. (2009). *The Probabilistic Relevance Framework: BM25 and Beyond.*
- Caselaw Access Project, Harvard Law School Library — corpus source.

## License

MIT. All corpus documents are public-domain US court opinions; per-document provenance in `data/sources.json` (v0.1) and `data/v0.3/sources.json` (v0.3).


## How to cite

Archived on Zenodo: [10.5281/zenodo.21969577](https://doi.org/10.5281/zenodo.21969577) (concept DOI, all versions). Cite the version you used; v0.3 adds the 150-item CourtListener set.

```bibtex
@software{nomi_crosssource,
  author    = {Nomi, Zoeb},
  title     = {CrossSource: an evaluation harness and dataset for citation accuracy of legal RAG on public case law},
  version   = {0.3},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.21969577},
  url       = {https://doi.org/10.5281/zenodo.21969577},
  license   = {MIT}
}
```

Opinion text: CourtListener, Free Law Project (v0.3); Caselaw Access Project, Harvard Law School Library (v0.1).
