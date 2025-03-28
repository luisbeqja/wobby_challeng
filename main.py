import json
from scripts.extract_pdf_text import PDFTranscriptReader
from scripts.filter_questions_regex import extract_questions_from_messages_regex

def main():
    pdf_path = "assets/Wobby AI Demo.pdf"

    # TODO: use LLM to auto detect the speaker
    # Set the speaker name of which you want to extract messages
    target_speaker = "Tove Staaf"
    
    # Create PDF reader instance and process the transcript
    pdf_reader = PDFTranscriptReader(pdf_path)
    user_messages = pdf_reader.filter_messages_by_speaker(target_speaker)
    
    # Extract questions from the messages
    questions = extract_questions_from_messages_regex(user_messages)
    
    # Save output to a JSON file
    output_filename = "data/user_messages_questions.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    

if __name__ == "__main__":
    main()
