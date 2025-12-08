import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY missing in .env")

genai.configure(api_key=API_KEY)

LLM_MODEL = "models/gemini-2.5-flash"

model = genai.GenerativeModel(LLM_MODEL)


def synthesize_answer(query: str, chunks: list[str]) -> str:
    context = "\n\n".join(chunks)

    prompt = f"""
Use ONLY the following context to answer.

QUESTION:
{query}

CONTEXT:
{context}

If the answer is not in the context, reply exactly:
"No relevant information found."
"""

    try:
        resp = model.generate_content(prompt)
        return resp.text
    except Exception as e:
        return f"LLM Error: {str(e)}"
