"""
Chunking via LlamaIndex's SentenceSplitter (llama-index-core only —
we don't pull in the rest of the LlamaIndex framework).

SentenceSplitter respects sentence boundaries where possible instead of
cutting mid-sentence, which matters for retrieval quality on policy /
legal-style text.
"""
from llama_index.core.node_parser import SentenceSplitter
from app.config import CHUNK_SIZE, CHUNK_OVERLAP

_splitter = SentenceSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
)


def chunk_text(text: str) -> list[str]:
    """Split raw text into a list of chunk strings."""
    if not text or not text.strip():
        return []
    return _splitter.split_text(text)
