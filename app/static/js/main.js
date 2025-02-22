function addMessage(message, isUser) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.style.opacity = '0';
    messageDiv.style.transform = 'translateY(20px)';
    messageDiv.textContent = message;
    messagesDiv.appendChild(messageDiv);
    
    // Trigger animation
    setTimeout(() => {
        messageDiv.style.transition = 'all 0.3s ease';
        messageDiv.style.opacity = '1';
        messageDiv.style.transform = 'translateY(0)';
    }, 100);
    
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const query = input.value.trim();
    const button = document.querySelector('.chat-input button');
    
    if (!query) return;
    
    // Disable input and button while processing
    input.disabled = true;
    button.disabled = true;
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
    
    // Add user message
    addMessage(query, true);
    input.value = '';
    
    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        addMessage(data.response, false);
    } catch (error) {
        addMessage('Sorry, there was an error processing your request.', false);
    } finally {
        // Re-enable input and button
        input.disabled = false;
        button.disabled = false;
        button.innerHTML = '<i class="fas fa-paper-plane"></i>';
        input.focus();
    }
}

// Allow Enter key to send messages
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Focus input on page load
window.addEventListener('load', function() {
    document.getElementById('user-input').focus();
}); 