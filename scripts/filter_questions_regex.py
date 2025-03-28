import re

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
