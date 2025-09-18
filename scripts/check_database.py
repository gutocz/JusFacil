import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

# --- Configurações ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PERSIST_DIR = str(PROJECT_ROOT / "db" / "chroma")
MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "laws"
QUERY_TEXT = "qual o direito do consumidor"

def main():
    """
    Script para verificar a base de dados ChromaDB e testar a busca semântica.
    """
    print("--- Iniciando verificação da base de conhecimento ---")

    # 1. Conectar ao banco de dados ChromaDB
    try:
        client = chromadb.PersistentClient(path=PERSIST_DIR)
        collection = client.get_collection(name=COLLECTION_NAME)
        print(f"✅ Conectado à coleção '{COLLECTION_NAME}' com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao conectar ao ChromaDB: {e}")
        print("Certifique-se de que o script 'build_database.py' foi executado primeiro.")
        return

    # 2. Verificar a quantidade de itens na coleção
    count = collection.count()
    print(f"📊 A coleção contém {count} documentos.")

    if count == 0:
        print("⚠️ A base de dados está vazia. Execute 'build_database.py' para populá-la.")
        return

    # 3. Realizar uma busca de teste
    print(f"\n🔎 Realizando busca de teste com a frase: '{QUERY_TEXT}'")
    
    # Carregar o modelo de embedding
    try:
        model = SentenceTransformer(MODEL_NAME)
        print("✅ Modelo de embedding carregado.")
    except Exception as e:
        print(f"❌ Erro ao carregar o modelo '{MODEL_NAME}': {e}")
        return

    # Converter a query em um embedding
    query_embedding = model.encode([QUERY_TEXT])[0].tolist()

    # Realizar a busca na coleção
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3,  # Pedir os 3 resultados mais relevantes
        include=["documents", "metadatas", "distances"]
    )

    # 4. Exibir os resultados
    if not results or not results.get("documents"):
        print("❌ A busca não retornou resultados.")
        return

    print("\n--- Resultados da Busca ---")
    for i, doc in enumerate(results["documents"][0]):
        distance = results["distances"][0][i]
        metadata = results["metadatas"][0][i]
        
        print(f"\nResultado {i+1} (Distância: {distance:.4f}):")
        print(f"  Fonte: {metadata.get('source', 'N/A')}")
        print(f"  Trecho: \"{doc}...\"") # Mostra o início do trecho

    print("\n--- Verificação concluída ---")

if __name__ == "__main__":
    main()
