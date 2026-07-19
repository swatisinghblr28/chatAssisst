"""
Wraps the local, persistent ChromaDB collection.
Everything lives on disk under data/index/chroma — no server to run.
"""
import chromadb
from app.config import CHROMA_DIR, CHROMA_COLLECTION

_client = chromadb.PersistentClient(path=CHROMA_DIR)
_collection = _client.get_or_create_collection(name=CHROMA_COLLECTION)


def add_chunks(ids: list[str], embeddings: list[list[float]],
               documents: list[str], metadatas: list[dict]) -> None:
    _collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )


def query(embedding: list[float], top_k: int) -> list[dict]:
    """Returns a list of {id, text, metadata, distance}, best first."""
    result = _collection.query(query_embeddings=[embedding], n_results=top_k)
    hits = []
    ids = result.get("ids", [[]])[0]
    docs = result.get("documents", [[]])[0]
    metas = result.get("metadatas", [[]])[0]
    dists = result.get("distances", [[]])[0]
    for i in range(len(ids)):
        hits.append({
            "id": ids[i],
            "text": docs[i],
            "metadata": metas[i],
            "distance": dists[i],
        })
    return hits


def count() -> int:
    return _collection.count()


def reset() -> None:
    """Drop and recreate the collection — wipes all vectors."""
    global _collection
    _client.delete_collection(name=CHROMA_COLLECTION)
    _collection = _client.get_or_create_collection(name=CHROMA_COLLECTION)
