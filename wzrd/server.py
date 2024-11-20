from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app)

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get('question')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400

        # Call the CLI with the question
        result = subprocess.run(['python', '../cli.py', 'ask-question', question], 
                              capture_output=True, 
                              text=True)
        
        # Return the CLI output
        return jsonify({'response': result.stdout.strip()})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
