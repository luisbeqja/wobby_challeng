from scripts.filter_questions_chain import filter_questions_chain

def main():
    pdf_path = "assets/Wobby AI Demo.pdf"

    # TODO: use LLM to auto detect the speakers
    # Set the speaker names of which you want to extract messages
    target_speakers = ["Tove Staaf", "Bruno Pauwels"]

    # Create PDF reader instance and process the transcript
    filter_questions_chain(pdf_path, target_speakers)
    
  
if __name__ == "__main__":
    main()
