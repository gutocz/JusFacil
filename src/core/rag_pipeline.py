# src/core/rag_pipeline.py
from typing import Dict, Any
import google.generativeai as genai

from dotenv import load_dotenv
load_dotenv()

from src import config
from src.data_processing.vector_store import search_knowledge_base

# --- Inicialização do Cliente da API ---
if not config.GOOGLE_API_KEY:
    raise ValueError("A chave da API do Google não foi encontrada. Defina a variável de ambiente GOOGLE_API_KEY no seu arquivo .env.")

genai.configure(api_key=config.GOOGLE_API_KEY)

# --- CORREÇÃO: Alterado o nome do modelo para a versão estável ---
_model = genai.GenerativeModel('gemini-2.5-flash')
# -------------------------------------------------------------

# --- Template do Prompt (sem alterações) ---
_PROMPT_TEMPLATE = """
Você é o "JusFácil", um assistente jurídico especializado em traduzir "juridiquês" 
para uma linguagem simples e acessível ao cidadão comum.

Sua tarefa é responder à pergunta do usuário de forma clara, objetiva e baseada 
EXCLUSIVAMENTE nos trechos da lei fornecidos no CONTEXTO.

REGRAS IMPORTANTES:
1.  **Baseie-se nos Fatos:** Responda apenas com informações contidas no CONTEXTO. Não use seu conhecimento prévio.
2.  **Seja Simples e Direto:** Evite jargões. Explique como se estivesse conversando com alguém sem nenhum conhecimento jurídico.
3.  **Cite a Fonte:** Se possível, mencione a fonte (ex: CLT, CDC) de onde a informação foi extraída.
4.  **Seja Cauteloso:** No final da resposta, inclua o aviso: "Esta é uma explicação simplificada e não substitui a consulta a um advogado."
5.  **Sem Informação:** Se o CONTEXTO não contiver a resposta, diga claramente: "Com base nos documentos fornecidos, não encontrei uma resposta direta para sua pergunta."

CONTEXTO:
{context}

PERGUNTA DO USUÁRIO:
{question}

RESPOSTA SIMPLIFICADA:
"""

def get_final_answer(query: str) -> Dict[str, Any]:
    """
    Orquestra o pipeline de RAG para obter uma resposta para a consulta do usuário.

    Args:
        query (str): A pergunta do usuário.

    Returns:
        Dict[str, Any]: Um dicionário contendo a resposta final e as fontes usadas.
    """
    # 1. Buscar na base de conhecimento
    search_results = search_knowledge_base(query, top_k=5)
    
    if not search_results:
        return {
            "answer": "Não foi possível encontrar informações relevantes nos documentos disponíveis para responder à sua pergunta.",
            "sources": []
        }

    # 2. Montar o Contexto
    context_chunks = [item['document'] for item in search_results]
    context_str = "\n---\n".join(context_chunks)

    # 3. Criar o Prompt Final
    final_prompt = _PROMPT_TEMPLATE.format(
        context=context_str,
        question=query
    )

    # 4. Chamar a API do Gemini
    try:
        response = _model.generate_content(final_prompt)
        answer = response.text
    except Exception as e:
        print(f"Erro ao chamar a API do Gemini: {e}")
        answer = "Desculpe, ocorreu um erro ao tentar gerar a resposta. Por favor, tente novamente."

    # 5. Estruturar e retornar o resultado final
    return {
        "answer": answer.strip(),
        "sources": search_results
    }