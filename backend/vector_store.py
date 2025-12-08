try:
    import chromadb
    from chromadb.config import Settings

    _client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="chroma_db"
    ))

    _collection = _client.get_or_create_collection(
        name="kb_docs",
        metadata={"hnsw:space": "cosine"}
    )

    def add_documents(documents: list[str], metadatas: list[dict], ids: list[str]):
        _collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        _client.persist()

    def query_documents(query: str, n_results: int = 5):
        result = _collection.query(
            query_texts=[query],
            n_results=n_results
        )
        docs = result["documents"][0]
        metas = result["metadatas"][0]
        ids = result["ids"][0]

        return list(zip(ids, docs, metas))
except Exception:
    # Fallback in-memory store for development when chromadb isn't installable
    _in_memory_store: list[tuple[str, str, dict]] = []

    def add_documents(documents: list[str], metadatas: list[dict], ids: list[str]):
        for _id, doc, meta in zip(ids, documents, metadatas):
            _in_memory_store.append((_id, doc, meta))

    def query_documents(query: str, n_results: int = 5):
        q = query.lower()
        matches: list[tuple[str, str, dict]] = []
        for _id, doc, meta in _in_memory_store:
            if q in doc.lower():
                matches.append((_id, doc, meta))
        return matches[:n_results]
