// Elementos DOM
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const loadingOverlay = document.getElementById('loadingOverlay');
const sourceModal = document.getElementById('sourceModal');
const modalBody = document.getElementById('modalBody');
const closeModal = document.getElementById('closeModal');
const charCount = document.querySelector('.char-count');

// Estado do chat
let isWaitingForResponse = false;

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    initializeChat();
    setupEventListeners();
});

function initializeChat() {
    // Auto-resize do textarea
    messageInput.addEventListener('input', function() {
        autoResizeTextarea(this);
        updateCharCount();
        updateSendButton();
    });
    
    // Enviar mensagem com Enter (sem Shift)
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!isWaitingForResponse && this.value.trim()) {
                sendMessage();
            }
        }
    });
    
    // Click nos exemplos de perguntas
    document.querySelectorAll('.example-questions li').forEach(item => {
        item.addEventListener('click', function() {
            messageInput.value = this.textContent.trim();
            updateCharCount();
            updateSendButton();
            messageInput.focus();
        });
    });
}

function setupEventListeners() {
    // Botão de enviar
    sendButton.addEventListener('click', sendMessage);
    
    // Fechar modal
    closeModal.addEventListener('click', hideSourceModal);
    
    // Fechar modal clicando fora
    sourceModal.addEventListener('click', function(e) {
        if (e.target === sourceModal) {
            hideSourceModal();
        }
    });
    
    // Fechar modal com ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && sourceModal.classList.contains('show')) {
            hideSourceModal();
        }
    });
}

function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
}

function updateCharCount() {
    const count = messageInput.value.length;
    charCount.textContent = `${count}/1000`;
    
    if (count > 900) {
        charCount.style.color = '#e53e3e';
    } else if (count > 700) {
        charCount.style.color = '#dd6b20';
    } else {
        charCount.style.color = '#718096';
    }
}

function updateSendButton() {
    const hasText = messageInput.value.trim().length > 0;
    sendButton.disabled = !hasText || isWaitingForResponse;
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || isWaitingForResponse) return;
    
    // Adicionar mensagem do usuário
    addMessage(message, 'user');
    
    // Limpar input
    messageInput.value = '';
    autoResizeTextarea(messageInput);
    updateCharCount();
    updateSendButton();
    
    // Mostrar loading
    showLoading();
    isWaitingForResponse = true;
    
    try {
        // Fazer requisição para a API
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: message })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Adicionar resposta do assistente
            addMessage(data.answer, 'assistant', data.sources);
        } else {
            // Mostrar erro
            addMessage(data.answer || 'Erro ao processar sua pergunta. Tente novamente.', 'assistant');
        }
    } catch (error) {
        console.error('Erro na requisição:', error);
        addMessage('Desculpe, ocorreu um erro de conexão. Verifique sua internet e tente novamente.', 'assistant');
    } finally {
        hideLoading();
        isWaitingForResponse = false;
        updateSendButton();
        messageInput.focus();
    }
}

function addMessage(text, sender, sources = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    // Header da mensagem
    const messageHeader = document.createElement('div');
    messageHeader.className = 'message-header';
    
    if (sender === 'user') {
        messageHeader.innerHTML = '<i class="fas fa-user"></i> Você';
    } else {
        messageHeader.innerHTML = '<i class="fas fa-robot"></i> JusFácil';
    }
    
    // Texto da mensagem
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = text;
    
    messageContent.appendChild(messageHeader);
    messageContent.appendChild(messageText);
    
    // Adicionar botão de fontes se existirem
    if (sources && sources.length > 0) {
        const sourcesDiv = document.createElement('div');
        sourcesDiv.className = 'message-sources';
        
        const sourcesButton = document.createElement('button');
        sourcesButton.className = 'sources-button';
        sourcesButton.innerHTML = '<i class="fas fa-book"></i> Ver fontes utilizadas';
        sourcesButton.addEventListener('click', () => showSourceModal(sources));
        
        sourcesDiv.appendChild(sourcesButton);
        messageContent.appendChild(sourcesDiv);
    }
    
    messageDiv.appendChild(messageContent);
    
    // Remover mensagem de boas-vindas se existir
    const welcomeMessage = chatMessages.querySelector('.welcome-message');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll para a última mensagem
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showSourceModal(sources) {
    modalBody.innerHTML = '';
    
    sources.forEach((source, index) => {
        const sourceDiv = document.createElement('div');
        sourceDiv.className = 'source-item';
        
        const title = document.createElement('div');
        title.className = 'source-title';
        title.textContent = `Fonte ${index + 1} - ${source.metadata?.source || 'Documento jurídico'}`;
        
        const content = document.createElement('div');
        content.className = 'source-content';
        content.textContent = source.document;
        
        sourceDiv.appendChild(title);
        sourceDiv.appendChild(content);
        modalBody.appendChild(sourceDiv);
    });
    
    sourceModal.classList.add('show');
}

function hideSourceModal() {
    sourceModal.classList.remove('show');
}

function showLoading() {
    loadingOverlay.classList.add('show');
}

function hideLoading() {
    loadingOverlay.classList.remove('show');
}

// Função para testar a conexão com a API
async function testConnection() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        console.log('API Status:', data);
    } catch (error) {
        console.error('Erro ao conectar com a API:', error);
    }
}

// Testar conexão ao carregar a página
testConnection();
