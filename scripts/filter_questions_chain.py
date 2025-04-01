"""
Chain of question extraction methods combining regex, spaCy, and LLM approaches.
"""
from scripts.extract_pdf_text import extract_messages_from_pdf
from scripts.filter_questions import extract_questions_from_messages_regex, extract_questions_from_messages_spacy
from llm.extract_question import extract_questions
import json
from typing import List, Dict


def filter_questions_chain(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Extract messages and questions from a PDF transcript using multiple methods.
    
    Args:
        pdf_path: Path to the PDF file
        target_speakers: List of speaker names to extract messages from
        
    Returns:
        List of non-question messages
    """
    
    
    # Extract questions using regex and spaCy
    regex_questions = extract_questions_from_messages_regex(messages)
    remaining_messages = [
        msg for msg in messages 
        if msg["message"] not in [q["message"] for q in regex_questions]
    ]
    spacy_questions = extract_questions_from_messages_spacy(remaining_messages)
    all_question_messages = regex_questions + spacy_questions
    
    # Filter out messages that contain questions
    non_question_messages = [
        msg for msg in messages 
        if msg["message"] not in [
            q.get("message", q.get("question", "")) for q in all_question_messages
        ]
    ]
    
    # Extract questions with LLM
    llm_questions = extract_questions(non_question_messages)
    
    # Combine all questions
    all_question_messages = all_question_messages + llm_questions
         
    return all_question_messages 