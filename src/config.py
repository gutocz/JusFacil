# src/config.py
import os
from pathlib import Path

# --- Caminhos Base ---
# Define a raiz do projeto dinamicamente
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_DIR = PROJECT_ROOT / "db" / "chroma"
DATA_DIR = PROJECT_ROOT / "data"

# --- Configurações do Banco de Dados Vetorial ---
PERSIST_DIRECTORY = str(DB_DIR)
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "laws")

# --- Configurações do Modelo de Embedding ---
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")