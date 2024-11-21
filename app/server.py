from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import sys
from pathlib import Path, PurePath
import logging

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

cli_path = PurePath(Path(__file__).parent.parent, 'cli', 'main.py')

@app.route('/import', methods=['POST'])
def import_resume():
    # Run import-resume with full error capture
    import_result = subprocess.run(
        [sys.executable, cli_path, 'import-resume'],
        capture_output=True,
        text=True,
        cwd=cli_path.parent     # Set working directory to CLI directory
    )
    if import_result.returncode != 0:
        app.logger.error(f"Import resume failed: {import_result.stderr}")
        return jsonify({'error': f'Import failed: {import_result.stderr}'}), 500
    return jsonify({'response': import_result.stdout.strip()})


@app.route('/ask', methods=['POST'])
def ask():
    try:

        # cli_path = PurePath(Path(__file__).parent.parent, 'cli', 'main.py')
        # app.logger.debug(f"CLI path: {cli_path}")
        
        # # Run import-resume with full error capture
        # import_result = subprocess.run(
        #     [sys.executable, cli_path, 'import-resume'],
        #     capture_output=True,
        #     text=True,
        #     cwd=cli_path.parent     # Set working directory to CLI directory
        # )
        # if import_result.returncode != 0:
        #     app.logger.error(f"Import resume failed: {import_result.stderr}")
        #     return jsonify({'error': f'Import failed: {import_result.stderr}'}), 500
        
        data = request.get_json()
        question = data.get('question')
        
        if not question:
            return jsonify({'error': 'No question provided'}), 400

        # Call the CLI with the question
        result = subprocess.run(
            [sys.executable, cli_path, 'ask-question', question],
            capture_output=True,
            text=True,
            cwd=cli_path.parent     # Set working directory to CLI directory
        )
        
        if result.returncode != 0:
            app.logger.error(f"Ask question failed: {result.stderr}")
            return jsonify({'error': f'Question processing failed: {result.stderr}'}), 500

        # Return the CLI output
        return jsonify({'response': result.stdout.strip()})
    
    except Exception as e:
        app.logger.error(f"Server error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    
    app.run(port=4000, debug=True)

    # # Run import-resume with full error capture
    # import_result = subprocess.run(
    #     [sys.executable, cli_path, 'import-resume'],
    #     capture_output=True,
    #     text=True,
    #     cwd=cli_path.parent     # Set working directory to CLI directory
    # )
    # if import_result.returncode != 0:
    #     app.logger.error(f"Import resume failed: {import_result.stderr}")
        # return jsonify({'error': f'Import failed: {import_result.stderr}'}), 500
