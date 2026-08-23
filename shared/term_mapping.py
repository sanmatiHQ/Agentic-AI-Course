"""Keyword and semantic vector maps for Concept Explainer search terms."""

from __future__ import annotations

import json
import re
from typing import Any

from shared.llm_providers import chat, embed_texts

TERM_MAP_PROMPT = """You map search terms to keywords and semantic neighbors.
Return ONLY valid JSON — an array with one object per input term:
[
  {
    "term": "RAG",
    "keywords": ["retrieval", "embeddings", "vector store", "grounding", "LLM"],
    "vector_neighbors": [
      {"label": "semantic search", "score": 0.91},
      {"label": "knowledge base QA", "score": 0.87}
    ]
  }
]
Rules:
- keywords: exactly 5 concise strings per term
- vector_neighbors: 5 related concepts with score 0.00-1.00 (higher = closer)
- one object per term, same order as input
"""


def split_search_terms(concept: str) -> list[str]:
    parts = [p.strip() for p in concept.replace(";", ",").split(",") if p.strip()]
    return parts or [concept.strip()]


def _parse_maps(raw: str, terms: list[str]) -> list[dict[str, Any]]:
    text = raw.strip()
    match = re.search(r"\[[\s\S]*\]", text)
    if match:
        text = match.group(0)
    try:
        data = json.loads(text)
        if isinstance(data, list) and data:
            return data
    except json.JSONDecodeError:
        pass
    return [{"term": t, "keywords": [], "vector_neighbors": []} for t in terms]


def _maps_via_llm(provider: str, api_key: str, model: str, terms: list[str]) -> list[dict[str, Any]]:
    user_msg = f"Search terms:\n" + "\n".join(f"- {t}" for t in terms)
    raw = chat(
        provider=provider,
        api_key=api_key,
        model=model,
        messages=[{"role": "user", "content": user_msg}],
        system=TERM_MAP_PROMPT,
        max_tokens=900,
    ).content
    return _parse_maps(raw, terms)


def _maps_via_embeddings(api_key: str, terms: list[str]) -> list[dict[str, Any]]:
    """OpenAI embeddings — real cosine similarity for vector neighbors."""
    seed_neighbors = [
        "semantic search",
        "knowledge graph",
        "fine-tuning",
        "prompt engineering",
        "agentic workflow",
        "vector database",
        "information retrieval",
        "transformer model",
        "embedding model",
        "grounded generation",
    ]
    results: list[dict[str, Any]] = []
    for term in terms:
        corpus = [term, *seed_neighbors]
        vectors = embed_texts(api_key, corpus)
        if not vectors:
            results.append({"term": term, "keywords": term.split()[:5], "vector_neighbors": []})
            continue
        base = vectors[0]
        scored = []
        for label, vec in zip(seed_neighbors, vectors[1:]):
            scored.append({"label": label, "score": round(_cosine(base, vec), 3)})
        scored.sort(key=lambda x: x["score"], reverse=True)
        keywords = [w for w in re.findall(r"[A-Za-z0-9\-\+]+", term) if len(w) > 2][:5]
        if len(keywords) < 3:
            keywords = [n["label"].split()[0] for n in scored[:5]]
        results.append(
            {
                "term": term,
                "keywords": keywords[:5],
                "vector_neighbors": scored[:5],
            }
        )
    return results


def _cosine(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(y * y for y in b) ** 0.5
    if not na or not nb:
        return 0.0
    return dot / (na * nb)


def build_term_maps(provider: str, api_key: str, model: str, concept: str) -> list[dict[str, Any]]:
    terms = split_search_terms(concept)
    if provider == "openai":
        try:
            return _maps_via_embeddings(api_key, terms)
        except Exception:
            pass
    return _maps_via_llm(provider, api_key, model, terms)


def term_maps_to_markdown(maps: list[dict[str, Any]]) -> str:
    if not maps:
        return ""
    lines = ["## Keyword & vector maps", ""]
    for item in maps:
        term = item.get("term", "")
        lines.append(f"### {term}")
        kws = item.get("keywords") or []
        if kws:
            lines.append("**Keywords:** " + ", ".join(f"`{k}`" for k in kws))
        neighbors = item.get("vector_neighbors") or []
        if neighbors:
            lines.append("")
            lines.append("| Semantic neighbor | Similarity |")
            lines.append("|---|---:|")
            for n in neighbors:
                lines.append(f"| {n.get('label', '')} | {n.get('score', 0):.2f} |")
        lines.append("")
    return "\n".join(lines)
