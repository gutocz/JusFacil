import os
import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb

sys.path.append(str(Path(__file__).resolve().parent.parent))
from src.data_processing.loader import load_pdf, split_into_chunks


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
PERSIST_DIR = str(PROJECT_ROOT / "db" / "chroma")
MODEL_NAME = "all-MiniLM-L6-v2"

print(f"[*] Raiz do projeto: {PROJECT_ROOT}")
print(f"[*] Diretório de dados: {DATA_DIR}")
print(f"[*] Diretório de persistência: {PERSIST_DIR}\n")

def main():
    client = chromadb.PersistentClient(path=PERSIST_DIR)

    collection = client.get_or_create_collection("laws")
    print(f"[*] Coleção '{collection.name}' acessada/criada.")

    model = SentenceTransformer(MODEL_NAME)

    print(f"[*] Procurando por arquivos PDF em '{DATA_DIR}'...")
    files_found = list(DATA_DIR.glob("*.pdf"))

    if not files_found:
        print(f"[!] Nenhum arquivo PDF encontrado. Verifique o diretório.")
        return

    print(f"[*] Encontrados {len(files_found)} arquivos: {[f.name for f in files_found]}")

    for file in files_found:
        print(f"\n--- Processando {file.name} ---")
        text = load_pdf(file)
        chunks = split_into_chunks(text)

        embeddings = model.encode(chunks, show_progress_bar=True)

        ids = [f"{file.stem}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": file.name, "chunk": i} for i in range(len(chunks))]

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

   
    print("\n✅ Base de conhecimento criada em db/chroma/")

if __name__ == "__main__":
    main()
