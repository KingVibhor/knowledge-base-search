import os
from typing import List, Dict

import chromadb
from .embeddings import embed_text, embed_texts

# Directory for persistent DB
DB_DIR = "data/vectorstore"
os.makedirs(DB_DIR, exist_ok=True)

# Create Chroma client
_client = chromadb.PersistentClient(path=DB_DIR)

# Always use this collection
_collection = _client.get_or_create_collection(
    name="kb_docs",
    metadata={"hnsw:space": "cosine"},
)


def add_documents(documents: List[str], metadatas: List[Dict], ids: List[str]) -> None:
    """Add text chunks + metadata + ids into ChromaDB."""

    if not documents:
        print("[WARN] add_documents called with 0 documents")
        return

    embeddings = embed_texts(documents)

    print(f"[INFO] ADDING DOCS: {len(documents)}")

    _collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings,
    )


def query_documents(query: str, top_k: int = 5):
    """Retrieve top K chunks for a given user query."""

    emb = embed_text(query)

    results = _collection.query(
        query_embeddings=[emb],
        n_results=top_k,
        include=["documents", "metadatas"]
    )

    docs = results["documents"][0] if results["documents"] else []
    metas = results["metadatas"][0] if results["metadatas"] else []

    combined = []
    for text, meta in zip(docs, metas):
        combined.append({
            "text": text,
            "source": meta.get("source"),
            "chunk_index": meta.get("chunk_index"),
        })

    return combined
