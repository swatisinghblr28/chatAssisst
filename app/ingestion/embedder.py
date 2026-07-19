"""
Thin wrapper around Ollama's embeddings endpoint.
Kept as its own module so swapping embedding backends later
(e.g. a different local model, or a hosted API in a future tenant
config) only touches this file.
"""
import ollama
from app.config import OLLAMA_HOST, EMBED_MODEL

_client = ollama.Client(host=OLLAMA_HOST)


def embed_text(text: str) -> list[float]:
    """Embed a single string. Ollama's embeddings API is single-input,
    so batch calls just loop this — fine at MVP scale."""
    response = _client.embeddings(model=EMBED_MODEL, prompt=text)
    return response["embedding"]


def embed_texts(texts: list[str]) -> list[list[float]]:
    return [embed_text(t) for t in texts]
