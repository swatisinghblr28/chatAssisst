# Hotel RAG MVP (Phase 1)

RAG chat assistant for a hotel client. Embeddings run locally through
[Ollama](https://ollama.com); answer generation uses the OpenAI API (GPT).
The Ollama-based generation path is kept in the code (commented out in
`app/generation/llm.py`) in case we switch back to a fully local LLM later.

## Stack
- **Backend:** FastAPI
- **LLM (generation):** OpenAI — `gpt-4o-mini` by default (swap in `app/config.py` / `OPENAI_MODEL` env var)
- **Embeddings:** Ollama — `nomic-embed-text` (local)
- **Vector store:** ChromaDB (local, persisted to `data/index/chroma`)
- **Keyword search:** BM25 (`rank_bm25`), corpus at `data/index/corpus.json`
- **Retrieval:** Hybrid — vector + BM25 combined via Reciprocal Rank Fusion
- **Chunking:** LlamaIndex `SentenceSplitter` (`llama-index-core`)
- **Frontend:** Minimal vanilla JS chat widget (`static/index.html`), admin upload UI (`static/admin.html`)

## Setup

1. **Install Ollama** (if you haven't): https://ollama.com/download — only needed for local embeddings.

2. **Pull the embedding model:**
   ```bash
   bash scripts/setup_ollama.sh
   ```
   (This also pulls a local LLM for the commented-out Ollama generation path — optional.)

3. **Set your OpenAI API key.** Create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=sk-...
   OPENAI_MODEL=gpt-4o-mini   # optional, this is the default
   ```

4. **Create a virtual environment and install dependencies:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Run the server:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

6. **Open the chat widget:** http://localhost:8000

## Ingest documents

**Option A — Admin UI:** go to **http://localhost:8000/admin**. Drag a file (or click to
browse), pick a document type, click "Ingest document." The ledger below shows
everything ingested so far, with chunk counts and timestamps.

**Option B — Terminal.** Upload any PDF/DOCX/HTML/TXT/MD file:

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@/path/to/your_hotel_policy.pdf" \
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
