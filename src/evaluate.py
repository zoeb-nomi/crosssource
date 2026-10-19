"""Scoring for CrossSource: four dimensions per (question, config) pair.

- citation_precision: of the citations given, fraction the judge verifies as
  actually supporting the claim they're attached to (checked against the cited
  chunk's text). Each failure gets a taxonomy label:
    wrong_document / right_doc_wrong_passage / unsupported_claim
- citation_recall: of the ground-truth supporting chunks, fraction cited
  (programmatic). Uncited ground-truth chunks are logged as missing_authority.
- faithfulness: fraction of the answer's claims supported by the retrieved
  context (RAGAS-style; Es et al., 2023).
- relevance: does the answer address the question (0 / 0.5 / 1).

Judge = an LLM with known caveats (Zheng et al., 2023); judge reliability is
itself measured against human labels in M5 (src/judge_check.py). Note the
judge and generator share a model family — a bias the M5 human check exists
to quantify.
"""

import json
import os
import re

from llm import complete

JUDGE_MODEL = os.environ.get("CROSSSOURCE_JUDGE_MODEL", "claude-opus-4-8")
CITATION_RE = re.compile(r"\[([a-z0-9_]+:\d+)\]")

VERDICT_SCHEMA = {
    "type": "json_schema",
    "schema": {
        "type": "object",
        "properties": {
            "supported": {"type": "boolean"},
            "failure_label": {
                "type": "string",
                "enum": ["right_doc_wrong_passage", "wrong_document", "unsupported_claim", "none"],
            },
            "reason": {"type": "string"},
        },
        "required": ["supported", "failure_label", "reason"],
        "additionalProperties": False,
    },
}

FAITHFULNESS_SCHEMA = {
    "type": "json_schema",
    "schema": {
        "type": "object",
        "properties": {
            "claims": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "claim": {"type": "string"},
                        "supported": {"type": "boolean"},
                    },
                    "required": ["claim", "supported"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["claims"],
        "additionalProperties": False,
    },
}

RELEVANCE_SCHEMA = {
    "type": "json_schema",
    "schema": {
        "type": "object",
        "properties": {
            "score": {"type": "string", "enum": ["0", "0.5", "1"]},
            "reason": {"type": "string"},
        },
        "required": ["score", "reason"],
        "additionalProperties": False,
    },
}


JUDGE_SYSTEM = "You are a meticulous auditor of a legal research assistant. Judge only from the text provided; never rely on outside knowledge."


def _judge(judge_model, prompt, schema):
    return json.loads(complete(judge_model, JUDGE_SYSTEM, prompt, 4000, schema=schema, role="judge"))


def citation_prompt(claim, cited_chunk, others):
    return f"""A legal research assistant answered a question and attached a citation to a claim.

CLAIM:
{claim}

CITED PASSAGE [{cited_chunk['id']}]:
{cited_chunk['text']}

OTHER PASSAGES THE ASSISTANT HAD AVAILABLE:
{context_block(others)}

Question 1: Does the CITED passage genuinely support the claim, such that a reader could verify the claim from that passage alone? (supported)
Question 2: If not supported, classify the failure:
- "right_doc_wrong_passage": another available passage from the SAME document supports the claim
- "wrong_document": an available passage from a DIFFERENT document supports the claim
- "unsupported_claim": no available passage supports the claim
Use "none" when supported is true."""


def judge_citation(judge_model, claim, cited_chunk, others):
    """One citation-precision verdict; also the task model for v0.3 citation_check items."""
    return _judge(judge_model, citation_prompt(claim, cited_chunk, others), VERDICT_SCHEMA)


def claim_citation_pairs(answer):
    """Pair each citation with the text span (claim) it is attached to."""
    pairs, last_end = [], 0
    for m in CITATION_RE.finditer(answer):
        claim = answer[last_end:m.start()].strip()
        # citations separated only by punctuation/whitespace ("[a:1], [a:2]")
        # are continuation citations for the previous claim span
        if not re.search(r"\w", claim) and pairs:
            claim = pairs[-1][0]
        # keep the claim to its last ~2 sentences for a focused judgment
        sentences = re.split(r"(?<=[.?!])\s+", claim)
        claim = " ".join(sentences[-2:]).strip()
        if re.search(r"\w", claim):
            pairs.append((claim, m.group(1)))
        last_end = m.end()
    return pairs


def context_block(chunks):
    return "\n\n".join(f"[{c['id']}]\n{c['text']}" for c in chunks)


def eval_item(item, generation, retrieved_chunks, judge_model=JUDGE_MODEL):
    """Score one (golden item, generated answer) pair. Returns a result dict."""
    answer = generation["answer"]
    chunk_by_id = {c["id"]: c for c in retrieved_chunks}
    pairs = claim_citation_pairs(answer)

    # --- citation precision + taxonomy ---
    citation_judgments = []
    for claim, cid in pairs:
        if cid not in chunk_by_id:
            citation_judgments.append({
                "claim": claim, "citation": cid, "supported": False,
                "failure_label": "unsupported_claim",
                "reason": "cited chunk was not in the retrieved set (fabricated or mis-copied id)",
            })
            continue
        others = [c for c in retrieved_chunks if c["id"] != cid]
        verdict = judge_citation(judge_model, claim, chunk_by_id[cid], others)
        citation_judgments.append({"claim": claim, "citation": cid, **verdict})

    supported_n = sum(1 for j in citation_judgments if j["supported"])
    citation_precision = supported_n / len(citation_judgments) if citation_judgments else 0.0

    # --- citation recall (programmatic) + missing_authority ---
    cited_ids = {cid for _, cid in pairs}
    truth = item["ground_truth_chunks"]
    hit = [t for t in truth if t in cited_ids]
    missing_authority = [t for t in truth if t not in cited_ids]
    citation_recall = len(hit) / len(truth) if truth else 0.0

    # --- faithfulness (RAGAS-style) ---
    faith = _judge(judge_model, f"""QUESTION:
{item['question']}

ASSISTANT'S ANSWER:
{answer}

RETRIEVED CONTEXT THE ASSISTANT WAS GIVEN:
{context_block(retrieved_chunks)}

List every distinct factual or legal claim the answer makes (short paraphrases).
For each, mark supported=true only if the retrieved context above supports it.""", FAITHFULNESS_SCHEMA)
    claims = faith["claims"]
    faithfulness = (sum(1 for c in claims if c["supported"]) / len(claims)) if claims else 0.0

    # --- relevance ---
    rel = _judge(judge_model, f"""QUESTION:
{item['question']}

ANSWER:
{answer}

Does the answer address what the question asks? "1" = directly addresses it,
"0.5" = partially addresses it, "0" = does not address it.""", RELEVANCE_SCHEMA)

    return {
        "id": item["id"],
        "config": generation["config"],
        "question": item["question"],
        "answer": answer,
        "citations": generation["citations"],
        "retrieved": generation["retrieved"],
        "ground_truth_chunks": truth,
        "citation_precision": round(citation_precision, 4),
        "citation_recall": round(citation_recall, 4),
        "faithfulness": round(faithfulness, 4),
        "relevance": float(rel["score"]),
        "relevance_reason": rel["reason"],
        "citation_judgments": citation_judgments,
        "missing_authority": missing_authority,
        "faithfulness_claims": claims,
    }
