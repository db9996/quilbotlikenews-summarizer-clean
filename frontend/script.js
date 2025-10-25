const API_URL = 'http://127.0.0.1:5000';

const newsInput = document.getElementById('newsInput');
const inputWordCount = document.getElementById('inputWordCount');
const summarizeBtn = document.getElementById('summarizeBtn');
const clearBtn = document.getElementById('clearBtn');
const wordLimit = document.getElementById('wordLimit');
const outputSection = document.getElementById('outputSection');
const summaryOutput = document.getElementById('summaryOutput');
const summaryWordCount = document.getElementById('summaryWordCount');
const loading = document.getElementById('loading');
const errorMessage = document.getElementById('errorMessage');
const copyBtn = document.getElementById('copyBtn');

// Update word count as user types
newsInput.addEventListener('input', () => {
    const text = newsInput.value.trim();
    const words = text ? text.split(/\s+/).length : 0;
    inputWordCount.textContent = `${words} words`;
});

// Summarize button
summarizeBtn.addEventListener('click', async () => {
    const text = newsInput.value.trim();
    const maxWords = parseInt(wordLimit.value);
    
    // Hide previous results
    outputSection.style.display = 'none';
    errorMessage.style.display = 'none';
    
    // Validation
    if (!text) {
        showError('Please enter some text to summarize.');
        return;
    }
    
    const wordCount = text.split(/\s+/).length;
    if (wordCount < 100) {
        showError(`Text is too short. Please enter at least 100 words. You have ${wordCount} words.`);
        return;
    }
    
    // Show loading
    loading.style.display = 'block';
    summarizeBtn.disabled = true;
    
    try {
        const response = await fetch(`${API_URL}/summarize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
                min_words: 50,
                max_words: maxWords
            })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            // Show summary
            summaryOutput.textContent = data.summary;
            summaryWordCount.textContent = `Summary: ${data.summary_words} words (Original: ${data.original_words} words)`;
            outputSection.style.display = 'block';
        } else {
            showError(data.error || 'Failed to summarize. Please try again.');
        }
    } catch (error) {
        showError('Connection error. Make sure the backend server is running.');
    } finally {
        loading.style.display = 'none';
        summarizeBtn.disabled = false;
    }
});

// Clear button
clearBtn.addEventListener('click', () => {
    newsInput.value = '';
    inputWordCount.textContent = '0 words';
    outputSection.style.display = 'none';
    errorMessage.style.display = 'none';
});

// Copy button
copyBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(summaryOutput.textContent);
    copyBtn.textContent = '✅ Copied!';
    setTimeout(() => {
        copyBtn.textContent = '📋 Copy';
    }, 2000);
});

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
}
