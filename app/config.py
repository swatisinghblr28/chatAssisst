"""
Central configuration for the Hotel RAG MVP.
Change model names / paths here as you tune the system.
"""
import os

# --- Ollama ---
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
LLM_MODEL = os.getenv("LLM_MODEL", "gemma:2b")          # try "qwen2.5:7b-instruct" as an alternative
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

# --- Chunking ---
CHUNK_SIZE = 500          # characters per chunk (tune based on your docs)
CHUNK_OVERLAP = 50

# --- Retrieval ---
VECTOR_TOP_K = 8           # candidates pulled from Chroma before fusion
KEYWORD_TOP_K = 8          # candidates pulled from BM25 before fusion
FINAL_TOP_K = 4            # chunks actually sent to the LLM as context
RRF_K = 60                 # reciprocal rank fusion constant (standard default)

# --- Storage paths ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DOCUMENTS_DIR = os.path.join(DATA_DIR, "documents")
CHROMA_DIR = os.path.join(DATA_DIR, "index", "chroma")
CORPUS_PATH = os.path.join(DATA_DIR, "index", "corpus.json")  # BM25 source-of-truth
CHROMA_COLLECTION = "hotel_docs"

os.makedirs(DOCUMENTS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(CHROMA_DIR), exist_ok=True)
