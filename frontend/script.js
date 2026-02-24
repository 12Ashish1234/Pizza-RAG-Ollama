const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const themeToggle = document.getElementById('theme-toggle');
const themeIconLight = document.getElementById('theme-icon-light');
const themeIconDark = document.getElementById('theme-icon-dark');

// Theme state initialization
function initTheme() {
    const savedTheme = localStorage.getItem('theme');

    // Check if the user has a saved theme, otherwise check OS preference
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcons(savedTheme);
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.setAttribute('data-theme', 'dark');
        updateThemeIcons('dark');
    }
}

function updateThemeIcons(theme) {
    if (theme === 'dark') {
        themeIconLight.style.display = 'none';
        themeIconDark.style.display = 'block';
    } else {
        themeIconLight.style.display = 'block';
        themeIconDark.style.display = 'none';
    }
}

// Toggle theme on click
themeToggle.addEventListener('click', () => {
    let currentTheme = document.documentElement.getAttribute('data-theme');
    let targetTheme = 'light';

    if (currentTheme !== 'dark') {
        targetTheme = 'dark';
    }

    // Toggle the theme with a brief transform scale animation
    themeIconLight.style.transform = 'scale(0)';
    themeIconDark.style.transform = 'scale(0)';

    setTimeout(() => {
        document.documentElement.setAttribute('data-theme', targetTheme);
        localStorage.setItem('theme', targetTheme);
        updateThemeIcons(targetTheme);

        themeIconLight.style.transform = 'scale(1)';
        themeIconDark.style.transform = 'scale(1)';
    }, 150); // Small delay to sync with CSS flip
});

initTheme();

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
