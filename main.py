from scripts.filter_questions_chain import filter_questions_chain
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from scripts.extract_pdf_text import extract_messages_from_pdf, filter_messages_by_speakers
from llm.categorize_questions import categorize_questions_with_options_list
from llm.leaderboard_generation import group_and_rank_questions

app = Flask(__name__)
CORS(app)

available_categories = ["Text-to-SQL", "Data Analysis", "Surveys", "Technical Questions", "General Discussion", "Pricing", "Integration"]

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload/text', methods=['POST'])
def upload_text():
    try:
        data = request.json 
        text = data.get('text')
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'questions.txt')
        messages = filter_messages_by_speakers(text, ['Stefan Debois', 'Bruno Pauwels'])
        
        with open(filename, 'w') as f:
            f.write(text)

        return jsonify({
            "message": "File uploaded successfully",
            "filename": 'questions.txt',
            "path": filename,
            "results": messages
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload/pdf', methods=['POST'])
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

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        questions = filter_questions_chain(data['messages'])
        categorized_questions = categorize_questions_with_options_list(questions, available_categories)
        return jsonify({"message": "Analysis requested", "data": categorized_questions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/leaderboard', methods=['POST'])
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
