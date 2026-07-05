"""Chunking + BM25 retrieval over the CrossSource corpus.

Chunk IDs are `doc_id:chunk_id` (e.g. brown_v_board:3) and are the unit of
ground truth for the golden set and of citation in generated answers.

IMPORTANT: chunking must stay deterministic and unchanged once the golden set
(data/golden.jsonl) is authored — golden ground-truth chunk IDs are positional.

Usage:  python src/retrieval.py "What standard governs stop and frisk?"
"""

import re
import sys
from pathlib import Path

from rank_bm25 import BM25Okapi

CORPUS_DIR = Path(__file__).resolve().parent.parent / "data" / "corpus"
TARGET_WORDS = 350  # ~500 tokens
MAX_WORDS = 450


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def chunk_text(text: str) -> list[str]:
    """Pack paragraphs into ~TARGET_WORDS chunks; hard-split oversized paragraphs."""
    units = []
    for para in re.split(r"\n+", text):
        para = para.strip()
        if not para:
            continue
        words = para.split()
        if len(words) > MAX_WORDS:
            units.extend(" ".join(words[i : i + TARGET_WORDS]) for i in range(0, len(words), TARGET_WORDS))
        else:
            units.append(para)

    chunks, current, count = [], [], 0
    for unit in units:
        n = len(unit.split())
        if current and count + n > TARGET_WORDS:
            chunks.append("\n".join(current))
            current, count = [], 0
        current.append(unit)
        count += n
    if current:
        chunks.append("\n".join(current))
    return chunks


class Retriever:
    def __init__(self, corpus_dir: Path = CORPUS_DIR):
        self.chunks = []  # list of {"id", "doc_id", "chunk_id", "text"}
        for path in sorted(corpus_dir.glob("*.txt")):
            doc_id = path.stem
            for i, text in enumerate(chunk_text(path.read_text(encoding="utf-8"))):
                self.chunks.append({"id": f"{doc_id}:{i}", "doc_id": doc_id, "chunk_id": i, "text": text})
        if not self.chunks:
            raise RuntimeError(f"no corpus files in {corpus_dir} — run src/fetch_corpus.py first")
        self.bm25 = BM25Okapi([tokenize(c["text"]) for c in self.chunks])

    def retrieve(self, query: str, k: int = 5) -> list[dict]:
        scores = self.bm25.get_scores(tokenize(query))
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [{**self.chunks[i], "score": float(scores[i])} for i in ranked]

    def get(self, chunk_id: str) -> dict | None:
        return next((c for c in self.chunks if c["id"] == chunk_id), None)


def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "What standard governs stop and frisk?"
    r = Retriever()
    print(f"{len(r.chunks)} chunks from {len({c['doc_id'] for c in r.chunks})} docs\n")
    for hit in r.retrieve(query):
        preview = " ".join(hit["text"].split())[:160]
        print(f"[{hit['id']}]  score={hit['score']:.2f}\n  {preview}...\n")


if __name__ == "__main__":
    main()
