from typing import List
import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

PERSIST_DIR = os.getenv("PERSIST_DIR", "./db/chroma")
MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

client = chromadb.Client(Settings(
    persist_directory="./db/chroma"  # diretório onde os dados serão salvos
))

_collection = client.get_or_create_collection("laws")
_model = SentenceTransformer(MODEL_NAME)

def search_knowledge_base(query: str, top_k: int = 5) -> List[str]:
    if not query.strip():
        return []

    query_emb = _model.encode([query]).tolist()
    results = _collection.query(
        query_embeddings=query_emb,
        n_results=top_k,
        include=["documents", "metadatas"]
    )

    chunks = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        artigo = meta.get("article", "Trecho")
        fonte = meta.get("source", "desconhecido")
        texto = doc.strip().replace("\n", " ")
        chunk = f"{artigo} — {texto} (Fonte: {fonte})"
        chunks.append(chunk)
    return chunks
