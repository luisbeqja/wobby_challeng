import re
import spacy

def extract_questions_from_messages_regex(messages):
    """
    Extract messages that are questions using a regex approach.
    This function checks if the message ends with a '?' character.
    """
    questions = []
    # Compile a regex that ensures the text ends with a question mark (possibly followed by whitespace)
    pattern = re.compile(r'\?\s*$')
    
    for message in messages:
        text = message["message"].strip()
        # If the message ends with a '?' according to our regex, consider it a question
        if pattern.search(text):
            questions.append(message)
    return questions



def extract_questions_from_messages_spacy(messages):
    """
    Extract messages that are questions using spaCy.
    """
    
    # Sample data (replace with the provided data list)
    data = messages

    # Load the spaCy English model
    nlp = spacy.load("en_core_web_sm")

    # Define question starters (wh-words and auxiliary verbs)
    question_starters = {
        'what', 'where', 'when', 'why', 'how', 'who', 'whom', 'which', 'whose',
        'do', 'does', 'did', 'is', 'am', 'are', 'was', 'were', 'have', 'has', 'had',
        'can', 'could', 'will', 'would', 'shall', 'should', 'may', 'might', 'must'
    }

    def is_question(sentence):
        """Determine if a sentence is a question."""
        stripped = sentence.text.strip()
        # Check if ends with a question mark
        if stripped.endswith('?'):
            return True
        # Check if starts with a question word/auxiliary
        tokens = [token.text.lower() for token in sentence]
        return tokens and tokens[0] in question_starters

    def extract_questions(messages):
        """Extract questions from the list of messages."""
        questions = []
        for entry in messages:
            doc = nlp(entry["message"])
            for sent in doc.sents:
                if is_question(sent):
                    questions.append({
                        "speaker": entry["speaker"],
                        "timestamp": entry["timestamp"],
                        "message": sent.text.strip()
                    })
        return questions

    # Extract and print questions
    extracted_questions = extract_questions(data)
    return extracted_questions
