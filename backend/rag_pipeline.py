import os
import uuid
from .utils.pdf_parser import extract_text_from_pdf
from .vector_store import add_documents, query_documents

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

def chunk_text(text: str) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end]
        chunks.append(chunk)
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks

def ingest_document(file_path: str, filename: str):
    if filename.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    chunks = chunk_text(text)

    ids = [str(uuid.uuid4()) for _ in chunks]
    metadatas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]

    add_documents(documents=chunks, metadatas=metadatas, ids=ids)

def retrieve_context(query: str, top_k: int = 5):
    return query_documents(query, n_results=top_k)
