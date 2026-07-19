#!/bin/bash
# Pulls the local models this project uses.
# Requires Ollama installed and running: https://ollama.com/download
set -e

echo "Pulling LLM (llama3.1:8b)..."
ollama pull llama3.1:8b

echo "Pulling embedding model (nomic-embed-text)..."
ollama pull nomic-embed-text

echo "Done. Verify with: ollama list"
