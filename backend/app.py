from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Load Hugging Face token from environment (.env file must set HF_TOKEN)
HF_TOKEN = os.getenv('HF_TOKEN')
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable is not set! Please set it in your .env file.")

# Use a fast model for reliable results
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

client = InferenceClient(token=HF_TOKEN)
print(f"✓ Hugging Face client initialized successfully with model: {MODEL_NAME}")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Quilbot News Summarizer API',
        'status': 'running'
    })

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.json
        text = data.get('text', '').strip()
        min_words = data.get('min_words', 50)
        max_words = data.get('max_words', 100)
        
        # Validation
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        word_count = len(text.split())
        if word_count < 100:
            return jsonify({'error': f'Text too short. Need at least 100 words. Got {word_count} words.'}), 400
        
        print(f"Summarizing {word_count} words...")

        # Summarize using fast DistilBART model
        result = client.summarization(
            text,
            model=MODEL_NAME
        )
        
        # Handle all result types
        summary_text = result.get('summary_text') if isinstance(result, dict) else result
        summary_words = len(summary_text.split())
        
        print(f"✓ Summary generated: {summary_words} words")
        
        return jsonify({
            'success': True,
            'summary': summary_text,
            'original_words': word_count,
            'summary_words': summary_words
        })
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
