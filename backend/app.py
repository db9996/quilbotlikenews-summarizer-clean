from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env file

app = Flask(__name__)
CORS(app)

HF_TOKEN = os.getenv('HF_TOKEN', '')
client = InferenceClient(token=HF_TOKEN)

print("✓ Hugging Face client initialized successfully!")

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

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        word_count = len(text.split())
        if word_count < 100:
            return jsonify({'error': f'Text too short. Need at least 100 words. Got {word_count} words.'}), 400

        print(f"Summarizing {word_count} words...")
        summary = client.summarization(
            text,
            model="facebook/bart-large-cnn"
        )

        summary_text = summary['summary_text']
        print(f"✓ Summary generated: {len(summary_text.split())} words")

        return jsonify({
            'success': True,
            'summary': summary_text,
            'original_words': word_count,
            'summary_words': len(summary_text.split())
        })

    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
