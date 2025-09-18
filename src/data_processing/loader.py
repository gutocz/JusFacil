from pathlib import Path
from pypdf import PdfReader
import unicodedata
import re

def load_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = [p.extract_text() or "" for p in reader.pages]
    text = "\n".join(pages)
    return normalize_text(text)


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def split_into_chunks(text: str, chunk_size: int = 2000, overlap: int = 200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    return chunks
