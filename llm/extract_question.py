import os
import google.generativeai as genai
import json
from typing import List, Dict


api_key = os.getenv('GEMINI_API_KEY')

# Configure the API
genai.configure(api_key=api_key)

def extract_questions(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:

    prompt = """
    Extract all questions from the following messages and return them as a structured list with the format:
    {
        "speaker": "Speaker Name",
        "timestamp": "HH:MM:SS",
        "message": "The extracted question"
    }
    
    Messages:
    """ + "\n".join([f"{msg['timestamp']} {msg['speaker']}: {msg['message']}" for msg in messages]) + """
    """
    
    
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content(prompt)

    try:
        clean_text = response.text.strip()
        if clean_text.startswith('```json'):
            clean_text = clean_text[7:]
        if clean_text.endswith('```'):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()
        
        
        questions = json.loads(clean_text)
        if isinstance(questions, list):
            return questions
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Raw response: {response.text}")
    
    return []