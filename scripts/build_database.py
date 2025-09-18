# scripts/build_database.py
import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

# Adiciona o diretório 'src' ao path para permitir importações diretas
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.data_processing.loader import load_pdf, split_into_chunks
from src import config  # Importa as configurações centralizadas

def main():
    """
    Constrói a base de dados vetorial a partir dos arquivos PDF no diretório de dados.
    """
    print(f"[*] Raiz do projeto: {config.PROJECT_ROOT}")
    print(f"[*] Diretório de dados: {config.DATA_DIR}")
    print(f"[*] Diretório de persistência: {config.PERSIST_DIRECTORY}\n")

    # 1. Conectar ao ChromaDB usando o caminho do arquivo de configuração
    client = chromadb.PersistentClient(path=config.PERSIST_DIRECTORY)
    collection = client.get_or_create_collection(config.COLLECTION_NAME)
    print(f"[*] Coleção '{collection.name}' acessada/criada.")

    # 2. Carregar o modelo de embedding
    model = SentenceTransformer(config.EMBEDDING_MODEL)

    # 3. Encontrar e processar arquivos PDF
    print(f"[*] Procurando por arquivos PDF em '{config.DATA_DIR}'...")
    files_found = list(config.DATA_DIR.glob("*.pdf"))

    if not files_found:
        print(f"[!] Nenhum arquivo PDF encontrado. Verifique o diretório.")
        return

    print(f"[*] Encontrados {len(files_found)} arquivos: {[f.name for f in files_found]}")

    for file in files_found:
        print(f"\n--- Processando {file.name} ---")
        text = load_pdf(file)
        chunks = split_into_chunks(text)

        embeddings = model.encode(chunks, show_progress_bar=True)
        
        # Gera IDs e metadados para cada chunk
        ids = [f"{file.stem}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": file.name, "chunk_index": i} for i in range(len(chunks))]

        # 4. Adicionar os dados à coleção
        collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        print(f"[*] {len(chunks)} chunks de '{file.name}' adicionados à coleção.")

    print("\n[*] Verificando a contagem final de documentos na coleção...")
    count = collection.count()
    print(f"[*] A coleção '{collection.name}' contém {count} documentos.")
    print(f"\n✅ Base de conhecimento criada em '{config.PERSIST_DIRECTORY}'")

if __name__ == "__main__":
    main()