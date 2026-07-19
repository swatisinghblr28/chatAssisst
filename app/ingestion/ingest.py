"""
End-to-end ingestion: parse -> chunk -> embed -> store (Chroma + BM25 corpus).
"""
import uuid
from datetime import datetime, timezone
from app.ingestion.parser import parse_file
from app.ingestion.chunker import chunk_text
from app.ingestion.embedder import embed_texts
from app.retrieval import vector_store, keyword_search


def ingest_file(file_path: str, source_name: str, doc_type: str = "general") -> int:
    """
    Ingest a single file into the knowledge base.
    doc_type is free-form metadata (e.g. "policy", "faq", "local_guide")
    useful later for metadata-filtered retrieval.
    Returns the number of chunks ingested.
    """
    text = parse_file(file_path)
    chunks = chunk_text(text)
    if not chunks:
        return 0

    embeddings = embed_texts(chunks)

    ids = [str(uuid.uuid4()) for _ in chunks]
    ingested_at = datetime.now(timezone.utc).isoformat()
    metadatas = [
        {"source": source_name, "doc_type": doc_type, "ingested_at": ingested_at}
        for _ in chunks
    ]

    vector_store.add_chunks(ids=ids, embeddings=embeddings, documents=chunks, metadatas=metadatas)

    keyword_search.append_to_corpus([
        {"id": ids[i], "text": chunks[i], "metadata": metadatas[i]}
        for i in range(len(chunks))
    ])

    return len(chunks)
