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
        "question": "The extracted question"
    }
    
    Messages:
    """ + "\n".join([f"{msg['timestamp']} {msg['speaker']}: {msg['message']}" for msg in messages]) + """
    """
    
    
    model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
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

if __name__ == "__main__":
    messages = [
        {"speaker": "Bruno Pauwels", "timestamp": "01:00:00", "content": "Can, you can probably flatten it out into a few kind of things."},
        {"speaker": "Alice Smith", "timestamp": "01:05:30", "content": "What do you think about the new design?"},
        {"speaker": "John Doe", "timestamp": "01:10:15", "content": "We should review the proposal."},
        {"speaker": "Bruno Pauwels", "timestamp": "01:15:45", "content": "Do you have any updates on the project?"}
    ]
    
    extracted_questions = extract_questions(messages)
    print(extracted_questions)