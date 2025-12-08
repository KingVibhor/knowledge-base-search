import uuid
from typing import List

import pdfplumber
import docx
from pdf2image import convert_from_path
import pytesseract

from .vector_store import add_documents, query_documents


# ---------- TEXT EXTRACTION ---------- #

def extract_text_pdf(path: str) -> str:
    print(f"[INFO] Extracting PDF text from: {path}")
    text_pages = []

    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_pages.append(t)
    except Exception as e:
        print("[ERROR] pdfplumber failed:", e)

    raw_text = "\n".join(text_pages)

    if raw_text.strip():
        return raw_text

    print("[WARN] PDF has no text. Trying OCR...")
    ocr_pages = []
    try:
        images = convert_from_path(path)
        for img in images:
            ocr_pages.append(pytesseract.image_to_string(img))
    except Exception as e:
        print("[ERROR] OCR pipeline failed:", e)

    return "\n".join(ocr_pages)


def extract_text_docx(path: str) -> str:
    try:
        d = docx.Document(path)
        return "\n".join(p.text for p in d.paragraphs if p.text.strip())
    except:
        return ""


def extract_text_txt(path: str) -> str:
    try:
        return open(path, "r", encoding="utf-8").read()
    except:
        return open(path, "r", encoding="latin-1").read()


def extract_text_image(path: str) -> str:
    try:
        return pytesseract.image_to_string(path)
    except:
        return ""


def extract_text(path: str) -> str:
    ext = path.lower().split(".")[-1]
    if ext == "pdf":
        return extract_text_pdf(path)
    if ext == "docx":
        return extract_text_docx(path)
    if ext == "txt":
        return extract_text_txt(path)
    if ext in ("png", "jpg", "jpeg"):
        return extract_text_image(path)
    return ""


# ---------- CHUNKING ---------- #

def chunk_text(text: str, chunk_size: int = 500) -> List[str]:
    if not text.strip():
        return []
    words = text.split()
    return [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


# ---------- INGESTION ---------- #

def ingest_document(path: str, filename: str) -> None:
    text = extract_text(path)

    if not text.strip():
        print("[ERROR] No text extracted. Nothing ingested.")
        return

    chunks = chunk_text(text)
    print(f"[INFO] CHUNKS CREATED: {len(chunks)}")

    ids = [str(uuid.uuid4()) for _ in chunks]
    metas = [{"source": filename, "chunk_index": i} for i in range(len(chunks))]

    add_documents(chunks, metas, ids)


# ---------- RETRIEVAL ---------- #

def retrieve_context(query: str, top_k: int = 5):
    return query_documents(query, top_k)
