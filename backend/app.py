from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
import os

from .rag_pipeline import ingest_document, retrieve_context
from .llm_client import synthesize_answer

app = FastAPI()

print(">>> CORS LOADED <<<")

# Proper CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# OPTIONS handler for browsers
@app.options("/{path:path}")
async def preflight_handler(path: str):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "*",
    }
    return Response(status_code=200, headers=headers)


@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    ingest_document(file_path, file.filename)
    return {"status": "success", "filename": file.filename}


@app.post("/query")
async def query_api(query: str = Form(...)):
    retrieved = retrieve_context(query, top_k=5)

    if not retrieved:
        return {"answer": "No relevant information found.", "sources": []}

    # retrieved = list of dicts → extract text chunks
    docs = [item["text"] for item in retrieved]

    # Gemini synthesis
    answer = synthesize_answer(query, docs)

    # Pass metadata + text back to frontend
    sources = [
        {
            "source": item["source"],
            "chunk_index": item["chunk_index"],
            "text": item["text"],
        }
        for item in retrieved
    ]

    return {"answer": answer, "sources": sources}
