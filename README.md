# JusFácil - Assistente Jurídico Inteligente

O JusFácil é um chatbot jurídico que utiliza inteligência artificial para responder dúvidas sobre direitos trabalhistas (CLT) e do consumidor (CDC) de forma simples e acessível.

## 🚀 Funcionalidades

- **Chat Inteligente**: Interface web moderna para interação com o assistente jurídico
- **RAG Pipeline**: Busca semântica em documentos jurídicos (CLT e CDC)
- **Respostas Simplificadas**: Tradução de "juridiquês" para linguagem acessível
- **Fontes Transparentes**: Exibição dos trechos das leis utilizados nas respostas
- **Design Responsivo**: Interface adaptável para desktop e mobile

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Flask**: Framework web para API
- **ChromaDB**: Banco de dados vetorial
- **Sentence Transformers**: Modelos de embedding
- **Google Gemini**: LLM para geração de respostas

### Frontend
- **HTML5/CSS3/JavaScript**: Interface web moderna
- **Font Awesome**: Ícones
- **Google Fonts**: Tipografia (Inter)

## 📋 Pré-requisitos

1. **Python 3.8 ou superior**
2. **Chave da API do Google Gemini**
3. **Base de dados vetorial** (gerada pelos scripts de processamento)

## 🔧 Instalação

1. **Clone o repositório**:
```bash
git clone https://github.com/gutocz/JusFacil.git
cd JusFacil
```

2. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**:
Crie um arquivo `.env` na raiz do projeto:
```env
GOOGLE_API_KEY=sua_chave_da_api_do_google_aqui
COLLECTION_NAME=nome_da_coleção (opcional)
EMBEDDING_MODEL=seu modelo para embedding (opcional)
```

4. **Gere a base de dados vetorial** (se ainda não foi feito):
```bash
python scripts/build_database.py
```

## 🚀 Como Executar

1. **Inicie o servidor Flask**:
```bash
python app.py
```

2. **Acesse a aplicação**:
Abra seu navegador e acesse: `http://localhost:5000`

## 📱 Como Usar

1. **Faça sua pergunta**: Digite uma pergunta jurídica na caixa de texto
2. **Aguarde a resposta**: O sistema buscará informações relevantes e gerará uma resposta simplificada
3. **Consulte as fontes**: Clique em "Ver fontes utilizadas" para ver os trechos das leis utilizados
4. **Continue conversando**: Faça novas perguntas para esclarecer dúvidas

### Exemplos de Perguntas

- "Quais são meus direitos quando sou demitido sem justa causa?"
- "O que fazer se o produto que comprei está com defeito?"
- "Posso trabalhar horas extras sem receber adicional?"
- "Qual o prazo para devolver um produto comprado online?"

## 📁 Estrutura do Projeto

```
JusFacil/
├── app.py                 # Servidor Flask principal
├── requirements.txt      # Dependências Python
├── README.md            # Este arquivo
├── .env                 # Variáveis de ambiente (criar)
├── data/                # PDFs das leis (CLT e CDC)
├── db/chroma/           # Base de dados vetorial
├── scripts/             # Scripts de processamento
├── src/                 # Código fonte Python
│   ├── config.py        # Configurações
│   ├── core/            # Pipeline RAG
│   └── data_processing/ # Processamento de dados
├── templates/           # Templates HTML
│   └── index.html       # Página principal
└── static/              # Arquivos estáticos
    ├── css/
    │   └── style.css    # Estilos CSS
    ├── js/
    │   └── script.js    # JavaScript do frontend
    └── images/          # Imagens (se houver)
```

## 🔍 Scripts Disponíveis

- `scripts/build_database.py`: Processa os PDFs e cria a base vetorial
- `scripts/check_database.py`: Verifica se a base de dados está funcionando
- `scripts/check_rag_pipeline.py`: Testa o pipeline RAG completo

## ⚠️ Aviso Legal

**IMPORTANTE**: Este sistema fornece informações jurídicas simplificadas baseadas em CLT e CDC, mas **NÃO substitui a consulta a um advogado qualificado**. Sempre consulte um profissional para questões jurídicas específicas.

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 🆘 Suporte

Se encontrar problemas:

1. Verifique se todas as dependências estão instaladas
2. Confirme se a chave da API do Google está configurada
3. Verifique se a base de dados vetorial foi gerada corretamente
4. Consulte os logs do servidor para mensagens de erro

Para dúvidas ou suporte, abra uma issue no repositório.
