# import ollama
# from app.config import OLLAMA_HOST, OPENAI_MODEL
from openai import OpenAI
from app.config import OPENAI_API_KEY, OPENAI_MODEL

from app.generation.prompt import SYSTEM_PROMPT, build_prompt

# _client = ollama.Client(host=OLLAMA_HOST)
_client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(query: str, chunks: list[dict]) -> str:
    user_prompt = build_prompt(query, chunks)

    # response = _client.chat(
    #     model=OPENAI_MODEL,
    #     messages=[
    #         {"role": "system", "content": SYSTEM_PROMPT},
    #         {"role": "user", "content": user_prompt},
    #     ],
    # )
    # return response["message"]["content"]

    response = _client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content
