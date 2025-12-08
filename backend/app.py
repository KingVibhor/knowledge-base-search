import os
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .rag_pipeline import ingest_document, retrieve_context
from .llm_client import synthesize_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "data/docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
        return JSONResponse({
            "answer": "No relevant information found.",
            "sources": []
        })

    ids, docs, metas = zip(*retrieved)
    answer = synthesize_answer(query, list(docs))

    sources = [
        {
            "source": m["source"],
            "chunk_index": m["chunk_index"],
            "text": d
        }
        for d, m in zip(docs, metas)
    ]

    return {
        "answer": answer,
        "sources": sources
    }
