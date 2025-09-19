# scripts/build_database.py
import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.data_processing.loader import load_and_split_pdf
from src import config

def main():
    """
    Constrói a base de dados vetorial a partir dos arquivos PDF.
    """
    print(f"[*] Diretório de persistência: {config.PERSIST_DIRECTORY}\n")

    client = chromadb.PersistentClient(path=config.PERSIST_DIRECTORY)
    
    # Apaga a coleção antiga para garantir que estamos reconstruindo com dados limpos
    print(f"[*] Tentando apagar a coleção antiga '{config.COLLECTION_NAME}' para uma reconstrução limpa...")
    try:
        client.delete_collection(name=config.COLLECTION_NAME)
        print(f"[*] Coleção antiga apagada com sucesso.")
    except Exception as e:
        print(f"[*] Nenhuma coleção antiga encontrada, criando uma nova.")

    collection = client.create_collection(config.COLLECTION_NAME)
    print(f"[*] Nova coleção '{collection.name}' criada.")

    model = SentenceTransformer(config.EMBEDDING_MODEL)

    print(f"[*] Procurando por arquivos PDF em '{config.DATA_DIR}'...")
    files_found = list(config.DATA_DIR.glob("*.pdf"))

    if not files_found:
        print(f"[!] Nenhum arquivo PDF encontrado.")
        return

    print(f"[*] Encontrados {len(files_found)} arquivos: {[f.name for f in files_found]}")

    for file in files_found:
        print(f"\n--- Processando {file.name} ---")
        chunks = load_and_split_pdf(file)

        if not chunks:
            print(f"[!] Nenhum chunk de texto foi extraído de {file.name}. Pulando.")
            continue

        embeddings = model.encode(chunks, show_progress_bar=True)
        ids = [f"{file.stem}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": file.name, "chunk_index": i} for i in range(len(chunks))]

        collection.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        print(f"[*] {len(chunks)} chunks de '{file.name}' adicionados à coleção.")

    count = collection.count()
    print(f"\n[*] A coleção '{collection.name}' agora contém {count} documentos.")
    print(f"\n✅ Base de conhecimento reconstruída em '{config.PERSIST_DIRECTORY}'")

if __name__ == "__main__":
    main()