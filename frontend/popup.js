document.addEventListener('DOMContentLoaded', async () => {
    const noVideoEl = document.getElementById('no-video');
    const contentEl = document.getElementById('content');
    const processBtn = document.getElementById('process-btn');
    const chatHistoryEl = document.getElementById('chat-history');
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const typingIndicator = document.querySelector('.typing-indicator');

    let videoId = null;
    let videoUrl = null;
    let isProcessed = false;
    let history = [];

    // Get current tab URL
    try {
        const tabs = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
        const url = tabs[0]?.url || '';
        console.log('Current tab URL:', url);

        const youtubeRegex = /^https:\/\/(?:www\.)?youtube\.com\/watch\?v=([\w-]{11})/;
        const match = url.match(youtubeRegex);

        if (match && match[1]) {
            videoId = match[1];
            videoUrl = `https://www.youtube.com/watch?v=${videoId}`;
            noVideoEl.classList.add('hidden');
            contentEl.classList.remove('hidden');

            // Load processing status and history
            const storageData = await chrome.storage.local.get([`${videoId}_processed`, `${videoId}_history`]);
            isProcessed = storageData[`${videoId}_processed`] || false;
            history = storageData[`${videoId}_history`] || [];
            console.log('Loaded history:', history);

            updateUI();
        } else {
            noVideoEl.classList.remove('hidden');
            contentEl.classList.add('hidden');
            console.log('Not a YouTube video page');
        }
    } catch (error) {
        console.error('Error checking URL:', error);
        noVideoEl.classList.remove('hidden');
        contentEl.classList.add('hidden');
    }

    function updateUI() {
        if (isProcessed) {
            processBtn.classList.add('hidden');
            messageInput.disabled = false;
            sendBtn.disabled = false;
            displayHistory();
        } else {
            processBtn.classList.remove('hidden');
            messageInput.disabled = true;
            sendBtn.disabled = true;
        }
    }

    function displayHistory() {
        chatHistoryEl.innerHTML = '';
        
        if (history.length === 0) {
            chatHistoryEl.innerHTML = `
                <div class="empty-chat">
                    <div class="empty-chat-icon">💬</div>
                    <div>Start a conversation about this video!</div>
                </div>
            `;
            return;
        }
        
        history.forEach(msg => {
            const msgEl = document.createElement('div');
            msgEl.classList.add('message', msg.role);
            
            const contentEl = document.createElement('div');
            contentEl.classList.add('message-content');
            contentEl.textContent = msg.content;
            
            msgEl.appendChild(contentEl);
            chatHistoryEl.appendChild(msgEl);
        });
        
        chatHistoryEl.scrollTop = chatHistoryEl.scrollHeight;
    }

    function showTypingIndicator() {
        typingIndicator.style.display = 'block';
        chatHistoryEl.scrollTop = chatHistoryEl.scrollHeight;
    }

    function hideTypingIndicator() {
        typingIndicator.style.display = 'none';
    }

    async function saveHistory() {
        try {
            await chrome.storage.local.set({ [`${videoId}_history`]: history });
            console.log('History saved:', history);
        } catch (error) {
            console.error('Error saving history:', error);
        }
    }

    // Enter key support for message input
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey && !sendBtn.disabled) {
            e.preventDefault();
            sendBtn.click();
        }
    });

    processBtn.addEventListener('click', async () => {
        console.log('Process button clicked, sending request to:', videoUrl);
        
        // Update button state
        processBtn.disabled = true;
        processBtn.innerHTML = '⏳ Processing...';
        
        try {
            const response = await fetch('http://localhost:8000/process/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ video_url: videoUrl })
            });
            
            console.log('Process response status:', response.status);
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Process failed: ${errorText}`);
            }
            
            const data = await response.json();
            console.log('Process response data:', data);
            
            if (data.video_id === videoId) {
                isProcessed = true;
                await chrome.storage.local.set({ [`${videoId}_processed`]: true });
                updateUI();
            }
        } catch (error) {
            console.error('Process error:', error);
            alert(`Failed to process video: ${error.message}`);
            
            // Reset button state on error
            processBtn.disabled = false;
            processBtn.innerHTML = '🚀 Process Video';
        }
    });

    sendBtn.addEventListener('click', async () => {
        const prompt = messageInput.value.trim();
        if (!prompt || !isProcessed) {
            console.log('Invalid prompt or video not processed:', { prompt, isProcessed });
            return;
        }

        // Append user message
        history.push({ role: 'user', content: prompt });
        displayHistory();
        await saveHistory();
        messageInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Disable input while processing
        messageInput.disabled = true;
        sendBtn.disabled = true;
        
        console.log('Sending message:', prompt);

        try {
            let endpoint = history.length <= 2 ? 'http://localhost:8000/query/' : 'http://localhost:8000/chat/';
            let body = history.length <= 2 ? { query: prompt } : { prompt };

            console.log('Sending request to:', endpoint, 'with body:', body);
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            
            console.log('Response status:', response.status);
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`API call failed: ${errorText}`);
            }
            
            const data = await response.json();
            console.log('Response data:', data);

            // Append assistant response
            history.push({ role: 'assistant', content: data.response });
            hideTypingIndicator();
            displayHistory();
            await saveHistory();
        } catch (error) {
            console.error('Chat error:', error);
            hideTypingIndicator();
            alert(`Failed to send message: ${error.message}`);
        } finally {
            // Re-enable input
            messageInput.disabled = false;
            sendBtn.disabled = false;
            messageInput.focus();
        }
    });
});