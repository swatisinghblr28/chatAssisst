"""
Prompt construction. Kept separate from llm.py so tone/persona can
become per-tenant config in phase 2 without touching the LLM call code.
"""

SYSTEM_PROMPT = """You are a helpful hotel guest assistant. Answer the guest's \
question using ONLY the information in the provided context. Do not use \
outside knowledge.

Rules:
- If the answer is not in the context, say you don't have that information \
and suggest they contact the front desk. Do not guess.
- Cite the source of every claim using the bracketed number, like [1].
- Be concise and friendly, in the tone of a hotel concierge.
"""


def build_prompt(query: str, chunks: list[dict]) -> str:
    context_blocks = []
    for i, chunk in enumerate(chunks, start=1):
        source = chunk.get("metadata", {}).get("source", "unknown")
        context_blocks.append(f"[{i}] (source: {source})\n{chunk['text']}")

    context_str = "\n\n".join(context_blocks) if context_blocks else "No context retrieved."

    return f"""Context:
{context_str}

Guest question: {query}

Answer the guest's question using only the context above, citing sources like [1].
"""
