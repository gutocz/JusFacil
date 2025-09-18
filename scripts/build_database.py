import os
import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from src.data_processing.loader import load_pdf, split_into_chunks

sys.path.append(str(Path(__file__).resolve().parent.parent))


DATA_DIR = Path("./data")
PERSIST_DIR = "./db/chroma"
MODEL_NAME = "all-MiniLM-L6-v2"

def main():
    client = chromadb.Client(Settings(
    persist_directory="./db/chroma" 
))

    collection = client.get_or_create_collection("laws")

    model = SentenceTransformer(MODEL_NAME)

    for file in DATA_DIR.glob("*.pdf"):
        print(f"Processando {file.name}...")
        text = load_pdf(file)
        chunks = split_into_chunks(text)

        embeddings = model.encode(chunks, show_progress_bar=True)

        ids = [f"{file.stem}_{i}" for i in range(len(chunks))]
        metadatas = [{"source": file.name, "chunk": i} for i in range(len(chunks))]

        collection.add(
            documents=["Lei 1", "Lei 2"],
            metadatas=[{"origem": "CLT"}, {"origem": "CDC"}],
            ids=["id1", "id2"]
)

   
    print("✅ Base de conhecimento criada em db/chroma/")

if __name__ == "__main__":
    main()
