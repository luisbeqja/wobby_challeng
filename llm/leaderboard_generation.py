import json
import os
import google.generativeai as genai

api_key = os.getenv('GEMINI_API_KEY')


genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def group_and_rank_questions(messages):
    """Groups similar questions and ranks them by frequency using a single prompt."""
    try:
        
        prompt = f"""
        Group the following questions based on semantic similarity. 
        Return ONLY a JSON array of arrays, where each inner array contains similar questions.
        
        You have also to add a question that is a good representative of the questions in the list.
        
        Example format:
        [
          ["representative_question", "question1", "question2", "question3"],
          ["representative_question", "question4", "question5"],
          ["representative_question", "question6"]
        ]

        Questions to group:
        {json.dumps([msg["message"] for msg in messages], indent=2)}

        Return ONLY the JSON array, no other text:
        """

        response = model.generate_content(prompt)
        groups_json = response.text.strip()
        
        # Clean the response to ensure it's valid JSON
        # Remove any markdown code block markers if present
        groups_json = groups_json.replace('```json', '').replace('```', '').strip()
        
        try:
            # Parse the JSON response
            groups = json.loads(groups_json)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON response: {groups_json}")
            print(f"JSON Error: {str(e)}")
            return []

        # Format output for FAQ leaderboard
        faq_leaderboard = []
        for group in groups:
            if isinstance(group, list) and len(group) > 0:
                faq_leaderboard.append({
                    "representative_question": group[0],  # Use the first question as representative
                    "question_count": len(group),
                    "example_questions": group,
                })

        # Rank groups by question_count in descending order
        faq_leaderboard.sort(key=lambda x: x["question_count"], reverse=True)

        return faq_leaderboard

    except Exception as e:
        print(f"Error in group_and_rank_questions: {str(e)}")
        print(f"Data structure received: {messages}")
        return []
