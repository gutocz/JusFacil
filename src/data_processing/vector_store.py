# src/data_processing/vector_store.py
from typing import List, Dict, Any
import chromadb
from sentence_transformers import SentenceTransformer
from src import config  # Importa as configurações centralizadas

# --- Inicialização ---
# Carrega o cliente e o modelo uma única vez para maior eficiência
try:
    _client = chromadb.PersistentClient(path=config.PERSIST_DIRECTORY)
    _collection = _client.get_collection(name=config.COLLECTION_NAME)
    _model = SentenceTransformer(config.EMBEDDING_MODEL)
except Exception as e:
    print(f"Erro ao inicializar o Vector Store: {e}")
    _collection = None
    _model = None

# --- Interface Pública ---
def search_knowledge_base(query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Busca na base de conhecimento por trechos relevantes e retorna os dados brutos.

    Args:
        query (str): A pergunta do usuário.
        top_k (int): O número de resultados a serem retornados.

    Returns:
        List[Dict[str, Any]]: Uma lista de dicionários, cada um contendo
                               o 'documento' e seus 'metadados'.
    """
    if not query.strip() or _collection is None or _model is None:
        return []

    # 1. Converter a query em um embedding
    query_embedding = _model.encode([query]).tolist()

    # 2. Realizar a busca na coleção do ChromaDB
    results = _collection.query(
        query_embeddings=query_embedding,
        n_results=top_k,
        include=["documents", "metadatas"]
    )

    # 3. Estruturar e retornar os resultados brutos
    # A responsabilidade de formatar a saída agora é da camada que chama esta função.
    if not results or "documents" not in results:
        return []

    search_results = [
        {"document": doc, "metadata": meta}
        for doc, meta in zip(results["documents"][0], results["metadatas"][0])
    ]
    
    return search_results