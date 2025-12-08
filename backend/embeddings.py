import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY missing in .env")

genai.configure(api_key=API_KEY)

EMBED_MODEL = "models/text-embedding-004"


def embed_text(text: str):
    resp = genai.embed_content(
        model=EMBED_MODEL,
        content=text
    )
    return resp["embedding"]


def embed_texts(texts: list[str]):
    resp = genai.embed_content(
        model=EMBED_MODEL,
        content=texts
    )
    return resp["embedding"]
