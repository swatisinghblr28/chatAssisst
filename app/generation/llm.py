import ollama
from app.config import OLLAMA_HOST, LLM_MODEL
from app.generation.prompt import SYSTEM_PROMPT, build_prompt

_client = ollama.Client(host=OLLAMA_HOST)


def generate_answer(query: str, chunks: list[dict]) -> str:
    user_prompt = build_prompt(query, chunks)

    response = _client.chat(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response["message"]["content"]
