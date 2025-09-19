import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.core.rag_pipeline import get_final_answer
from src import config

# pergunta de exemplo
QUERY_TEXT = "Fui demitido sem justa causa, quais meus direitos?"

def main():
    """
    Script para testar o pipeline RAG completo com a API do Gemini.
    """
    print("--- Iniciando teste do Pipeline RAG ---")

    if not config.GOOGLE_API_KEY:
        print("\nERRO: A variável de ambiente GOOGLE_API_KEY não está configurada.")
        print("Por favor, crie um arquivo .env na raiz do projeto e adicione sua chave.")
        return

    print(f"\nEnviando a seguinte pergunta para o sistema:\n   '{QUERY_TEXT}'")
    print("\nAguarde, consultando a base de conhecimento e gerando a resposta com o Gemini...")

    try:
        result = get_final_answer(QUERY_TEXT)
    except Exception as e:
        print(f"\n❌ Ocorreu um erro durante a execução do pipeline: {e}")
        return
    
    print("\n" + "="*50)
    print("✅ Resposta Gerada pelo JusFácil (via Gemini):")
    print("="*50)
    print(result.get("answer", "Nenhuma resposta retornada."))
    
    print("\n" + "="*50)
    print("📚 Fontes Utilizadas (retornadas pela busca):")
    print("="*50)
    
    sources = result.get("sources", [])
    if not sources:
        print("Nenhuma fonte foi utilizada.")
    else:
        for i, source_item in enumerate(sources):
            source_doc = source_item.get("document", "Documento não encontrado")
            source_meta = source_item.get("metadata", {})
            source_file = source_meta.get("source", "Fonte desconhecida")
            
            print(f"\n--- Fonte {i+1} (de: {source_file}) ---")
            print(f"Trecho: \"{source_doc[:200]}...\"")

    print("\n--- Teste concluído ---")

if __name__ == "__main__":
    main()