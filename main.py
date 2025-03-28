import json
from scripts.extract_pdf_text import PDFTranscriptReader



def extract_messages_from_pdf(pdf_path, target_speakers):
    reader = PDFTranscriptReader(pdf_path)
    messages = reader.filter_messages_by_speakers(target_speakers)
    
    # Save all messages to a single JSON file
    output_filename = "data/transcript_messages.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False) 
         
    return messages


def main():
    pdf_path = "assets/Wobby AI Demo.pdf"

    # TODO: use LLM to auto detect the speakers
    # Set the speaker names of which you want to extract messages
    target_speakers = ["Tove Staaf", "Bruno Pauwels"]

    # Create PDF reader instance and process the transcript
    extract_messages_from_pdf(pdf_path, target_speakers)
    
  
if __name__ == "__main__":
    main()
