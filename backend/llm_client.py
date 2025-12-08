import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

def synthesize_answer(query: str, context_chunks: list[str]) -> str:
    context_text = "\n\n".join(
        [f"[Chunk {i+1}]\n{c}" for i, c in enumerate(context_chunks)]
    )

    prompt = f"""
You are a knowledge-base assistant.
Use ONLY the information provided in the context. 
If the answer is not present in the context, say "The answer is not available in the provided documents."

Context:
{context_text}

User Question:
{query}

Give a concise, factual answer.
"""

    response = model.generate_content(prompt)
    return response.text
