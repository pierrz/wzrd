from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
# Configure CORS to allow requests from the Vue dev server
CORS(app, resources={
    r"/ask": {
        "origins": [
            "http://localhost:5173",  # Vite dev server
            "http://localhost:3000"   # Production preview
        ],
        "methods": ["POST"],
        "allow_headers": ["Content-Type"]
    }
})

@app.route('/ask', methods=['POST'])
def ask():
    try:
        # subprocess.run(['ls'])
        subprocess.run(['uv', 'run', 'cli/main.py', 'import-resume'])
        
        data = request.get_json()
        question = data.get('question')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400

        # Call the CLI with the question
        result = subprocess.run(['uv', 'run', 'cli/main.py', 'ask-question', question], 
                              capture_output=True, 
                              text=True)
        
        # Return the CLI output
        return jsonify({'response': result.stdout.strip()})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=4000, debug=True)
