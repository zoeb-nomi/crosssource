"""RAG answer generation with inline [doc_id:chunk_id] citations.

Two configurations share one model and differ only in citation discipline:
  - baseline: told the citation format, nothing more
  - strict:   adds explicit citation-discipline rules
The eval harness (M4) compares the two on citation precision/recall,
faithfulness, and relevance.

Requires ANTHROPIC_API_KEY (env var or .env).

Usage:  python src/generate.py "What standard governs stop and frisk?"
"""

import os
import re
import sys

from dotenv import load_dotenv

from llm import complete
from retrieval import Retriever

load_dotenv()

MODEL = os.environ.get("CROSSSOURCE_MODEL", "claude-opus-4-8")
MAX_TOKENS = 1500
CITATION_RE = re.compile(r"\[([a-z0-9_]+):(\d+)\]")

FORMAT_RULES = """You are a legal research assistant answering questions about US court opinions.
You are given numbered excerpts from those opinions. Answer using the excerpts.
Cite sources inline by copying the bracketed excerpt ID exactly as given,
e.g. [brown_v_board:3]. Place citations immediately after the text they support."""

DISCIPLINE_RULES = """
Citation discipline — follow these rules exactly:
1. Every factual or legal claim in your answer must be followed by a citation
   to an excerpt whose text actually supports that specific claim.
2. Do not cite an excerpt for general relevance; cite it only if a reader could
   verify the claim by reading that excerpt alone.
3. If the excerpts do not contain the information needed to answer, say so
   explicitly. Never answer from outside knowledge and never invent citations.
4. Quote key legal language exactly where possible."""

CONFIGS = {
    "baseline": {"system": FORMAT_RULES},
    "strict": {"system": FORMAT_RULES + DISCIPLINE_RULES},
}


def build_prompt(question: str, chunks: list[dict]) -> str:
    blocks = [f"[{c['id']}]\n{c['text']}" for c in chunks]
    return "Excerpts from court opinions:\n\n" + "\n\n---\n\n".join(blocks) + f"\n\nQuestion: {question}"


def parse_citations(text: str) -> list[str]:
    seen = []
    for doc, chunk in CITATION_RE.findall(text):
        cid = f"{doc}:{chunk}"
        if cid not in seen:
            seen.append(cid)
    return seen


def answer(question: str, config: str, retriever: Retriever, model: str = MODEL, k: int = 5) -> dict:
    chunks = retriever.retrieve(question, k=k)
    text = complete(model, CONFIGS[config]["system"], build_prompt(question, chunks), MAX_TOKENS, role="generate")
    return {
        "question": question,
        "config": config,
        "model": model,
        "answer": text,
        "citations": parse_citations(text),
        "retrieved": [c["id"] for c in chunks],
    }


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is not set — add it to .env (see .env.example)")
    question = sys.argv[1] if len(sys.argv) > 1 else "What standard governs stop and frisk?"
    retriever = Retriever()
    for config in CONFIGS:
        result = answer(question, config, retriever)
        print(f"\n=== {config} ===\n{result['answer']}\n")
        print(f"parsed citations: {result['citations']}")
        print(f"retrieved:        {result['retrieved']}")


if __name__ == "__main__":
    main()
