import PyPDF2
import google.generativeai as genai
import json
import dotenv
import os

dotenv.load_dotenv()

# Configure the Gemini API with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def analyze_syllabus(syllabus_text):
    prompt = """
            You are an AI assistant tasked with extracting structured data from a syllabus. Follow these exact instructions:

            ### **Instructions**
            - Extract all **important dates** (tests, assignments, quizzes, etc.).
            - Extract all **weightings** for course components.
            - The output must strictly follow **this JSON structure**, with no additional text, comments, or explanations.
            - If a **time** is provided in the syllabus, format it as `"HH:MM:SS"`. If no time is given, set it to `null`.
            - If a date is missing, **exclude that entry**.
            - If a weighting percentage is missing, **exclude that entry**.
            - Always return **two separate JSON arrays** inside a single JSON object.

            {
            "important_dates": [
                {
                "title": "First Assignment Due",
                "date": "YYYY-MM-DD"
                },
                {
                "title": "Midterm Exam",
                "date": "YYYY-MM-DD"
                },
                ...
            ],
            "weightings": [
                {
                "component": "Assignments",
                "weight": "30%"
                },
                {
                "component": "Final Exam",
                "weight": "50%"
                },
                ...
            ]
            }

    """ 
    submit = prompt + syllabus_text

    model = genai.GenerativeModel("gemini-1.5-flash")
    print('started')
    response = model.generate_content(submit)
    print('got it')
    return response.text
    
    # Assuming the Gemini model returns the results in the desired format as text
    #return json.loads(response.text)


def save_to_files(important_dates_json, weightings_json):
    """
    Function to save the extracted important dates and course weightings into two separate files.
    """
    # Save important dates to a file
    with open("important_dates.json", "w") as f:
        json.dump(important_dates_json, f, indent=4)

    # Save course weightings to a file
    with open("course_weightings.json", "w") as f:
        json.dump(weightings_json, f, indent=4)


# Example usage
syllabus_text = """
Week 1:
- Lecture on AI basics (January 10, 2025)
- First Assignment Due: January 20, 2025 (11:59 PM)

Week 5:
- Midterm Exam: February 15, 2025 (10:00 AM)

Week 8:
- Final Exam: April 30, 2025 (2:00 PM)

Course components:
- Assignments: 30%
- Midterm Exam: 20%
- Final Exam: 50%
"""

# Step 1: Analyze the syllabus
# result = analyze_syllabus(syllabus_text)

# # Step 2: Separate and save the output into two different JSON files
# save_to_files(result['important_dates'], result['course_weightings'])

