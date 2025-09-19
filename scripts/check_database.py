import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.data_processing.vector_store import search_knowledge_base
from src import config

# Texto de exemplo
QUERY_TEXT = "qual o direito do consumidor em caso de produto com defeito"

def main():
    """
    Verifica a base de dados e testa a função de busca semântica.
    """
    print("--- Iniciando verificação da base de conhecimento ---")

    print(f"\n Realizando busca de teste com a frase: '{QUERY_TEXT}'")
    
    results = search_knowledge_base(QUERY_TEXT, top_k=3)

    if not results:
        print("A busca não retornou resultados.")
        print("Certifique-se de que o script 'build_database.py' foi executado.")
        return

    print("\n--- Resultados da Busca ---")
    for i, result in enumerate(results):
        doc = result.get("document", "N/A")
        meta = result.get("metadata", {})
        source = meta.get("source", "N/A")
        
        print(f"\nResultado {i+1}:")
        print(f"  Fonte: {source}")
        print(f"  Trecho: \"{doc[:150]}...\"") 

    print("\n✅ Verificação concluída com sucesso!")

if __name__ == "__main__":
    main()