"""
BM25 keyword search. Chroma doesn't do lexical/exact-term matching well,
so this covers the cases hotel guests actually type — room numbers,
exact policy names, dates — where semantic similarity alone misses.

The corpus (all chunk texts + metadata) lives in a flat JSON file that
ingestion appends to. The BM25 index is rebuilt from it on demand —
fine at MVP scale; revisit if the corpus grows past a few thousand chunks.
"""
import json
import os
from rank_bm25 import BM25Okapi
from app.config import CORPUS_PATH


def _load_corpus() -> list[dict]:
    if not os.path.exists(CORPUS_PATH):
        return []
    with open(CORPUS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def append_to_corpus(records: list[dict]) -> None:
    """records: list of {id, text, metadata}"""
    corpus = _load_corpus()
    corpus.extend(records)
    os.makedirs(os.path.dirname(CORPUS_PATH), exist_ok=True)
    with open(CORPUS_PATH, "w", encoding="utf-8") as f:
        json.dump(corpus, f)


def list_documents() -> list[dict]:
    """Group the flat chunk corpus by source file for display purposes."""
    corpus = _load_corpus()
    docs: dict[str, dict] = {}
    for item in corpus:
        meta = item.get("metadata", {})
        source = meta.get("source", "unknown")
        if source not in docs:
            docs[source] = {
                "source": source,
                "doc_type": meta.get("doc_type", "general"),
                "ingested_at": meta.get("ingested_at"),
                "chunk_count": 0,
            }
        docs[source]["chunk_count"] += 1
    return sorted(docs.values(), key=lambda d: d.get("ingested_at") or "", reverse=True)


def _tokenize(text: str) -> list[str]:
    return text.lower().split()


def search(query_text: str, top_k: int) -> list[dict]:
    corpus = _load_corpus()
    if not corpus:
        return []

    tokenized_corpus = [_tokenize(item["text"]) for item in corpus]
    bm25 = BM25Okapi(tokenized_corpus)
    scores = bm25.get_scores(_tokenize(query_text))

    ranked = sorted(
        zip(corpus, scores), key=lambda pair: pair[1], reverse=True
    )[:top_k]

    return [
        {"id": item["id"], "text": item["text"], "metadata": item["metadata"], "score": score}
        for item, score in ranked
        if score > 0
    ]
