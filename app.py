from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sys
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
sys.path.append(str(Path(__file__).resolve().parent))

from src.core.rag_pipeline import get_final_answer

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    """Página principal do chatbot"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Endpoint para receber perguntas e retornar respostas do chatbot jurídico
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                'error': 'Pergunta não fornecida',
                'answer': 'Por favor, forneça uma pergunta válida.'
            }), 400
        
        question = data['question'].strip()
        
        if not question:
            return jsonify({
                'error': 'Pergunta vazia',
                'answer': 'Por favor, digite sua pergunta.'
            }), 400
        
        # Chamar o pipeline RAG
        result = get_final_answer(question)
        
        # Formatar resposta para o frontend
        response = {
            'answer': result.get('answer', 'Não foi possível gerar uma resposta.'),
            'sources': result.get('sources', []),
            'question': question
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Erro no endpoint /api/chat: {e}")
        return jsonify({
            'error': 'Erro interno do servidor',
            'answer': 'Desculpe, ocorreu um erro ao processar sua pergunta. Tente novamente.'
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint para verificar se a API está funcionando"""
    return jsonify({
        'status': 'ok',
        'message': 'API do JusFácil está funcionando'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
