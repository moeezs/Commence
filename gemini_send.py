import google.generativeai as genai
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


