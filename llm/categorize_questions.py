import os
import google.generativeai as genai


api_key = os.getenv('GEMINI_API_KEY')
model = genai.GenerativeModel('gemini-2.0-flash')

def categorize_question_with_options(question_data, available_categories):
    """Categorizes a question using Gemini, choosing from a list of options."""

    category_list_str = ", ".join(available_categories)

    prompt = f"""
    Categorize the following question based on its main topic. 
    Choose a category from the following list: {category_list_str}.
    If the question is not related to any of the categories, choose "Other".
    Question: "{question_data['message']}"

    Category:
    """

    try:
        response = model.generate_content(prompt)

        category = response.text.strip()

        # Validate the category against the available options
        if category in available_categories:
            return category
        else:
            return "Other"  # Or handle invalid categories as needed
    except Exception as e:
        print(f"Error processing question: {e}")
        return "Unknown"

def categorize_questions_with_options_list(questions, available_categories):
    """Categorizes a list of questions and returns a list of dictionaries with categories."""
    categorized_questions = []
    for question in questions:
        category = categorize_question_with_options(question, available_categories)
        categorized_questions.append({
            "message": question["message"],
            "speaker": question["speaker"],
            "timestamp": question["timestamp"],
            "category": category
        })
    return categorized_questions


available_categories = ["Text-to-SQL", "Data Analysis", "Surveys", "Technical Questions", "General Discussion"] # Add your needed categories.