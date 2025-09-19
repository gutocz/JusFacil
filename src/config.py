import os
from pathlib import Path

# Caminhos Base
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_DIR = PROJECT_ROOT / "db" / "chroma"
DATA_DIR = PROJECT_ROOT / "data"

# Configurações do Banco de Dados Vetorial
PERSIST_DIRECTORY = str(DB_DIR)
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "laws")

# Configurações do Modelo de Embedding
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "paraphrase-multilingual-mpnet-base-v2")

# Configurações da API do LLM
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")