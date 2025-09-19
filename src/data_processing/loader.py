# src/data_processing/loader.py
from pathlib import Path
from pypdf import PdfReader
import unicodedata
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List

def load_and_split_pdf(path: Path, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
    """
    Carrega o texto de um arquivo PDF, limpa-o e o divide em chunks semânticos.

    Args:
        path (Path): O caminho para o arquivo PDF.
        chunk_size (int): O tamanho máximo de cada chunk.
        chunk_overlap (int): A sobreposição de caracteres entre chunks.

    Returns:
        List[str]: Uma lista de chunks de texto.
    """
    print(f"  -> Lendo arquivo: {path.name}")
    reader = PdfReader(str(path))
    pages = [p.extract_text() or "" for p in reader.pages]
    full_text = "\n".join(pages)

    # Etapa de limpeza mais robusta
    cleaned_text = _clean_text(full_text)
    
    # Usando o divisor de texto inteligente do LangChain
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""], # Tenta dividir por parágrafos primeiro
    )

    chunks = text_splitter.split_text(cleaned_text)
    print(f"  -> Arquivo dividido em {len(chunks)} chunks.")
    return chunks

def _clean_text(text: str) -> str:
    """Função interna para realizar uma limpeza mais profunda no texto extraído."""
    # Normaliza para remover caracteres estranhos e ligaduras
    text = unicodedata.normalize("NFKC", text)
    
    # Remove múltiplos espaços, mas mantém quebras de linha únicas
    text = re.sub(r" +", " ", text)
    # Tenta juntar palavras que foram quebradas com um hífen no final da linha
    text = re.sub(r"-\n", "", text)
    # Remove quebras de linha excessivas, mantendo no máximo duas (parágrafos)
    text = re.sub(r"\n{3,}", "\n\n", text)
    
    return text.strip()