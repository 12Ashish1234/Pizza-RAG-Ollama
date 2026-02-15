const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.textContent = content;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function addLoadingIndicator() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading-dots';
    loadingDiv.id = 'loading-indicator';
    loadingDiv.innerHTML = `
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    `;
    chatContainer.appendChild(loadingDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return loadingDiv;
}

function removeLoadingIndicator(indicator) {
    if (indicator) {
        indicator.remove();
    }
}

async function handleSendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Add user message
    addMessage(message, true);
    userInput.value = '';
    userInput.focus();

    // Add loading state
    const loadingIndicator = addLoadingIndicator();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: message }),
        });

        const data = await response.json();
        
        // Remove loading state
        removeLoadingIndicator(loadingIndicator);

        if (response.ok) {
            addMessage(data.answer);
        } else {
            addMessage('Error: Something went wrong. Please try again.');
            console.error('Server error:', data);
        }
    } catch (error) {
        removeLoadingIndicator(loadingIndicator);
        addMessage('Error: Could not connect to the server.');
        console.error('Connection error:', error);
    }
}

sendBtn.addEventListener('click', handleSendMessage);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        handleSendMessage();
    }
});

// Focus input on load
userInput.focus();
