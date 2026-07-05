# CrossSource

**An evaluation harness for RAG answer quality and citation accuracy on public case law.**

Legal AI is a major LLM category whose most famous trust failure is citation hallucination — lawyers have been sanctioned for filing AI-fabricated citations (*Mata v. Avianca*), and academic work (Stanford RegLab, "Hallucination-Free? Assessing the Reliability of Leading AI Legal Research Tools," Magesh et al., 2024) found even dedicated legal RAG tools hallucinate at meaningful rates. CrossSource is an open, reproducible harness for measuring citation-level reliability of a RAG system on public court opinions.

This project is an independent implementation of published RAG-evaluation methods — RAGAS-style faithfulness (Es et al., 2023), LLM-as-judge with known caveats (Zheng et al., 2023), and classic IR precision/recall — applied to a domain where citation errors carry professional consequences.

## Status

v0.1 in progress. Milestones: scaffold ✅ · corpus ✅ · pipeline ⬜ · golden set ⬜ · eval harness ⬜ · judge validation ⬜ · results + publish ⬜

## Corpus

22 famous, public-domain US court opinions (16 Supreme Court, 2 federal circuit, 4 state high court) spanning constitutional law, contracts, torts, employment, civil procedure, and consumer protection. Text from the [Caselaw Access Project](https://case.law) (Harvard Law School Library); every file's provenance is in `data/sources.json`. ~190k tokens total. The corpus deliberately contains no tax authorities. Note: CourtListener's REST API was the original source but now requires authentication for opinion text, so the fetch script uses CAP's public static files instead.

## License

MIT
