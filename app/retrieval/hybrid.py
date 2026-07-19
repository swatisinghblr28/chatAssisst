"""
Combines vector search and BM25 keyword search using Reciprocal Rank
Fusion (RRF) — simpler and more robust than trying to normalize and
weight two differently-scaled scores by hand.
"""
from app.ingestion.embedder import embed_text
from app.retrieval import vector_store, keyword_search
from app.config import VECTOR_TOP_K, KEYWORD_TOP_K, FINAL_TOP_K, RRF_K


def retrieve(query_text: str, top_k: int = FINAL_TOP_K) -> list[dict]:
    query_embedding = embed_text(query_text)

    vector_hits = vector_store.query(query_embedding, VECTOR_TOP_K)
    keyword_hits = keyword_search.search(query_text, KEYWORD_TOP_K)

    fused_scores: dict[str, float] = {}
    chunk_lookup: dict[str, dict] = {}

    for rank, hit in enumerate(vector_hits):
        fused_scores[hit["id"]] = fused_scores.get(hit["id"], 0) + 1 / (RRF_K + rank + 1)
        chunk_lookup[hit["id"]] = hit

    for rank, hit in enumerate(keyword_hits):
        fused_scores[hit["id"]] = fused_scores.get(hit["id"], 0) + 1 / (RRF_K + rank + 1)
        chunk_lookup.setdefault(hit["id"], hit)

    ranked_ids = sorted(fused_scores, key=lambda cid: fused_scores[cid], reverse=True)
    top_ids = ranked_ids[:top_k]

    return [chunk_lookup[cid] for cid in top_ids]
