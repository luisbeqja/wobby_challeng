import json
from scripts.extract_pdf_text import PDFTranscriptReader
from scripts.filter_questions import extract_questions_from_messages_spacy, extract_questions_from_messages_regex


def extract_messages_from_pdf(pdf_path, target_speakers):
    reader = PDFTranscriptReader(pdf_path)
    
    messages = reader.filter_messages_by_speakers(target_speakers)
    regex_questions = extract_questions_from_messages_regex(messages)
    
    # Filter out regex questions to get remaining messages
    remaining_messages = [
        msg for msg in messages 
        if msg["message"] not in [q["message"] for q in regex_questions]
    ]
    
    # Apply spaCy question detection on remaining messages
    spacy_questions = extract_questions_from_messages_spacy(remaining_messages)
    
    # Combine all question messages
    all_question_messages = regex_questions + spacy_questions
    
    # Filter out messages that contain questions (from either regex or spaCy)
    non_question_messages = [
        msg for msg in messages 
        if msg["message"] not in [
            q.get("message", q.get("question", "")) for q in all_question_messages
        ]
    ]
    
    # Save all messages to a single JSON file
    output_filename = "data/transcript_messages.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(non_question_messages, f, indent=2, ensure_ascii=False) 
    
    output_filename = "data/transcript_messages_questions.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(all_question_messages, f, indent=2, ensure_ascii=False)
         
    return non_question_messages


def main():
    pdf_path = "assets/Wobby AI Demo.pdf"

    # TODO: use LLM to auto detect the speakers
    # Set the speaker names of which you want to extract messages
    target_speakers = ["Tove Staaf", "Bruno Pauwels"]

    # Create PDF reader instance and process the transcript
    extract_messages_from_pdf(pdf_path, target_speakers)
    
  
if __name__ == "__main__":
    main()
