import os
import shutil
import uuid
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from app.config import DOCUMENTS_DIR
from app.ingestion.ingest import ingest_file
from app.retrieval.hybrid import retrieve
from app.retrieval import vector_store, keyword_search
from app.generation.llm import generate_answer

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...), doc_type: str = Form("general")):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in (".pdf", ".docx", ".html", ".htm", ".txt", ".md"):
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

    saved_name = f"{uuid.uuid4()}{ext}"
    saved_path = os.path.join(DOCUMENTS_DIR, saved_name)
    with open(saved_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        num_chunks = ingest_file(saved_path, source_name=file.filename, doc_type=doc_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {e}")

    return {"filename": file.filename, "doc_type": doc_type, "chunks_ingested": num_chunks}


class ChatRequest(BaseModel):
    query: str


@router.post("/chat")
async def chat(request: ChatRequest):
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    try:
        chunks = retrieve(request.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {e}")

    try:
        answer = generate_answer(request.query, chunks)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed (is Ollama running with the model pulled?): {e}")

    sources = [
        {"index": i + 1, "source": c.get("metadata", {}).get("source", "unknown"), "text": c["text"]}
        for i, c in enumerate(chunks)
    ]

    return {"answer": answer, "sources": sources}


@router.get("/status")
async def status():
    return {"indexed_chunks": vector_store.count()}


@router.get("/documents")
async def list_documents():
    return {"documents": keyword_search.list_documents()}


@router.delete("/documents")
async def clear_documents():
    """Wipe all ingested data: vector store, BM25 corpus, and saved upload files."""
    try:
        vector_store.reset()
        keyword_search.clear_corpus()
        for fname in os.listdir(DOCUMENTS_DIR):
            fpath = os.path.join(DOCUMENTS_DIR, fname)
            if os.path.isfile(fpath):
                os.remove(fpath)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset failed: {e}")

    return {"status": "cleared"}
