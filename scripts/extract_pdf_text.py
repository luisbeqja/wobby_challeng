import re
from PyPDF2 import PdfReader
from typing import List, Union

class PDFTranscriptReader:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.text = None
        self.messages = None

    def extract_text(self):
        """Extract text from the PDF file."""
        reader = PdfReader(self.pdf_path)
        self.text = ""
        for page in reader.pages:
            self.text += page.extract_text() + "\n"
        return self.text

    def parse_transcript(self):
        """
        Parse transcript text into a list of message dicts.
        Assumes each message block starts with a line like:
            Speaker Name - HH:MM[:SS]
        and the message text follows until the next speaker block.
        """
        if self.text is None:
            self.extract_text()

        # This pattern captures:
        #   group 'speaker': speaker's name (can include spaces and punctuation)
        #   group 'timestamp': a timestamp in format HH:MM or HH:MM:SS
        #   group 'message': message text until the next speaker block.
        pattern = re.compile(
            r"(?P<speaker>[A-Za-z\s]+)\s*-\s*(?P<timestamp>\d{2}:\d{2}(?::\d{2})?)\s*\n(?P<message>.*?)(?=\n[A-Za-z\s]+?\s*-\s*\d{2}:\d{2}(?::\d{2})?\s*\n|$)",
            re.DOTALL
        )
        self.messages = []
        for match in pattern.finditer(self.text):
            speaker = match.group("speaker").strip()
            timestamp = match.group("timestamp").strip()
            message = match.group("message").strip().replace("\n", " ")  # collapse newlines within message
            self.messages.append({
                "speaker": speaker,
                "timestamp": timestamp,
                "message": message
            })
        return self.messages

    def filter_messages_by_speakers(self, target_speakers: Union[str, List[str]]) -> List[dict]:
        """
        Filter messages for one or more speakers.
        
        Args:
            target_speakers: A single speaker name or a list of speaker names
            
        Returns:
            List of messages from the specified speakers
        """
        if self.messages is None:
            self.parse_transcript()
            
        # Convert single speaker to list for consistent processing
        if isinstance(target_speakers, str):
            target_speakers = [target_speakers]
            
        # Convert all speakers to lowercase for case-insensitive comparison
        target_speakers = [speaker.lower() for speaker in target_speakers]
        
        return [
            msg for msg in self.messages 
            if msg["speaker"].lower() in target_speakers
        ]