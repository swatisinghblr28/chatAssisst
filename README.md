# Hotel RAG MVP (Phase 1)

Fully local RAG chat assistant for a hotel client. No external API calls —
LLM and embeddings run through [Ollama](https://ollama.com).

## Stack
- **Backend:** FastAPI
- **LLM:** Ollama — `llama3.1:8b` (swap in `app/config.py`)
- **Embeddings:** Ollama — `nomic-embed-text`
- **Vector store:** ChromaDB (local, persisted to `data/index/chroma`)
- **Keyword search:** BM25 (`rank_bm25`), corpus at `data/index/corpus.json`
- **Retrieval:** Hybrid — vector + BM25 combined via Reciprocal Rank Fusion
- **Chunking:** LlamaIndex `SentenceSplitter` (`llama-index-core`)
- **Frontend:** Minimal vanilla JS chat widget (`static/index.html`)

## Setup

1. **Install Ollama** (if you haven't): https://ollama.com/download

2. **Pull the models:**
   ```bash
   bash scripts/setup_ollama.sh
   ```

3. **Create a virtual environment and install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

5. **Open the chat widget:** http://localhost:8000

## Ingest documents

**Option A — Admin UI:** go to **http://localhost:8000/admin**. Drag a file (or click to
browse), pick a document type, click "Ingest document." The ledger below shows
everything ingested so far, with chunk counts and timestamps.

**Option B — Terminal.** A sample hotel policy doc is included at
`data/documents/sample_hotel_policies.txt`:

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@data/documents/sample_hotel_policies.txt" \
  -F "doc_type=policy"
```

Check how much is indexed:
```bash
curl http://localhost:8000/api/status
curl http://localhost:8000/api/documents
```

## Ask a question

Either use the web widget at http://localhost:8000, or:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What time is check-in and is there an early check-in fee?"}'
```

## Where things live (for when you extend this)

| Want to change... | Edit... |
|---|---|
| Chunk size / overlap | `app/config.py` |
| Which local models are used | `app/config.py` |
| How documents are parsed | `app/ingestion/parser.py` |
| Chunking strategy | `app/ingestion/chunker.py` |
| Retrieval weighting / top-k | `app/config.py`, `app/retrieval/hybrid.py` |
| System prompt / persona / grounding rules | `app/generation/prompt.py` |
| API endpoints | `app/api/routes.py` |

## Next steps (per the phased plan)
- Build a 30–50 question test set from real hotel content and measure retrieval accuracy
- Add re-ranking on top of the fused hybrid results
- Get this in front of one real hotel client
- Only after that: move to Phase 2 (multi-tenancy, admin UI, config-driven guardrails)
