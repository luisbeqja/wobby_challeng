"""
PDF text extraction functionality.
"""
import re
from PyPDF2 import PdfReader
from typing import List, Union, Dict


def extract_text(pdf_path: str) -> str:
    """
    Extract text from the PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        The extracted text as a string
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def parse_transcript(text: str) -> List[Dict[str, str]]:
    """
    Parse transcript text into a list of message dicts.
    Assumes each message block starts with a line like:
        Speaker Name - HH:MM[:SS]
    and the message text follows until the next speaker block.
    
    Args:
        text: The transcript text to parse
        
    Returns:
        List of message dictionaries with speaker, timestamp, and message
    """
    # This pattern captures:
    #   group 'speaker': speaker's name (can include spaces and punctuation)
    #   group 'timestamp': a timestamp in format HH:MM or HH:MM:SS
    #   group 'message': message text until the next speaker block.
    pattern = re.compile(
        r"(?P<speaker>[A-Za-z\s]+)\s*-\s*(?P<timestamp>\d{2}:\d{2}(?::\d{2})?)\s*\n(?P<message>.*?)(?=\n[A-Za-z\s]+?\s*-\s*\d{2}:\d{2}(?::\d{2})?\s*\n|$)",
        re.DOTALL
    )
    
    messages = []
    for match in pattern.finditer(text):
        speaker = match.group("speaker").strip()
        timestamp = match.group("timestamp").strip()
        message = match.group("message").strip().replace("\n", " ")
        messages.append({
            "speaker": speaker,
            "timestamp": timestamp,
            "message": message
        })
    return messages


def filter_messages_by_speakers(messages: List[Dict[str, str]], target_speakers: Union[str, List[str]]) -> List[Dict[str, str]]:
    """
    Filter messages for one or more speakers.
    
    Args:
        messages: List of message dictionaries
        target_speakers: A single speaker name or a list of speaker names
        
    Returns:
        List of messages from the specified speakers
    """
    if isinstance(target_speakers, str):
        target_speakers = [target_speakers]
        
    target_speakers = [speaker.lower() for speaker in target_speakers]
    
    return [
        msg for msg in messages 
        if msg["speaker"].lower() in target_speakers
    ]


def extract_messages_from_pdf(pdf_path: str, target_speakers: Union[str, List[str]]) -> List[Dict[str, str]]:
    """
    Extract and filter messages from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        target_speakers: Speaker name(s) to filter for
        
    Returns:
        List of filtered message dictionaries
    """
    # Extract text from PDF
    text = extract_text(pdf_path)
    
    # Parse transcript into messages
    messages = parse_transcript(text)
    
    # Filter messages by speakers
    return filter_messages_by_speakers(messages, target_speakers)