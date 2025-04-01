from scripts.filter_questions_chain import filter_questions_chain
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from scripts.extract_pdf_text import extract_messages_from_pdf, filter_messages_by_speakers, parse_transcript
from llm.categorize_questions import categorize_questions_with_options_list
from llm.leaderboard_generation import group_and_rank_questions

# Get the absolute path to the client/dist directory
CLIENT_DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'client', 'dist')

app = Flask(__name__, static_folder=CLIENT_DIST, static_url_path='')
CORS(app)

available_categories = ["Text-to-SQL", "Data Analysis", "Surveys", "Technical Questions", "General Discussion", "Pricing", "Integration"]

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

# Handle client-side routing
@app.route('/<path:path>')
def static_proxy(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    return send_from_directory(app.static_folder, 'index.html')

# API Routes
@app.route('/api/upload/text', methods=['POST'])
def upload_text():
    try:
        data = request.json 
        if not data or 'text' not in data:
            return jsonify({"error": "No text provided in request"}), 400
            
        text = data['text']
        if not isinstance(text, str):
            return jsonify({"error": "Text must be a string"}), 400
            
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'questions.txt')
        
        # Parse the text into messages first
        messages = parse_transcript(text)
        filtered_messages = filter_messages_by_speakers(messages, ['Stefan Debois', 'Bruno Pauwels'])
        
        with open(filename, 'w') as f:
            f.write(text)

        return jsonify({
            "message": "File uploaded successfully",
            "filename": 'questions.txt',
            "path": filename,
            "results": filtered_messages
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/upload/pdf', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if not file.filename.endswith('.pdf'):
            return jsonify({"error": "Only PDF files are allowed"}), 400
        
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        # Extract text from PDF
        text = extract_messages_from_pdf(filename, ['Stefan Debois', 'Bruno Pauwels'])
        
        return jsonify({
            "message": "File uploaded successfully",
            "filename": file.filename,
            "path": filename,
            "results": text
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        questions = filter_questions_chain(data['messages'])
        categorized_questions = categorize_questions_with_options_list(questions, available_categories)
        return jsonify({"message": "Analysis requested", "data": categorized_questions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/leaderboard', methods=['POST'])
def leaderboard():
    try:
        data = request.json
        leaderboard = group_and_rank_questions(data['messages'])
        return jsonify({"message": "Leaderboard requested", "data": leaderboard}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def main():
    print(f"Files will be uploaded to: {UPLOAD_FOLDER}")
    app.run(debug=True)
  
if __name__ == "__main__":
    main()
