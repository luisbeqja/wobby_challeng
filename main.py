import json
from tools.pdf_reader import PDFTranscriptReader


def main():
    pdf_path = "assets/Wobby AI Demo.pdf"

    # TODO: use LLM to auto detect the speaker
    # Set the speaker name of which you want to extract messages
    target_speaker = "Tove Staaf"
    
    # Create PDF reader instance and process the transcript
    pdf_reader = PDFTranscriptReader(pdf_path)
    user_messages = pdf_reader.filter_messages_by_speaker(target_speaker)
    
    # Save output to a JSON file
    output_filename = "data/user_messages.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(user_messages, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(user_messages)} messages from speaker '{target_speaker}' saved to {output_filename}")


if __name__ == "__main__":
    main()
