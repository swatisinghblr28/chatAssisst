#!/bin/bash
# Pulls the local models this project uses.
# Requires Ollama installed and running: https://ollama.com/download
set -e

echo "Pulling LLM (gemma2:2b)..."
ollama pull gemma2:2b

echo "Pulling embedding model (nomic-embed-text)..."
ollama pull nomic-embed-text

echo "Done. Verify with: ollama list"
