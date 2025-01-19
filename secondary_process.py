import json
import re

def process_raw_response(response_text):
    # Remove any leading/trailing whitespace
    response_text = response_text.strip()
    
    # Try to find JSON-like sections using regex
    important_dates_match = re.search(r'\[.*?(\{.*?\}.*?)*\]', response_text, re.DOTALL)
    weightings_match = re.search(r'\[.*?(\{.*?\}.*?)*\]', 
                                 response_text[important_dates_match.end() if important_dates_match else 0:], 
                                 re.DOTALL)
    
    # Extract and parse JSON sections
    important_dates = []
    weightings = []
    
    if important_dates_match:
        try:
            important_dates = json.loads(important_dates_match.group(0))
        except json.JSONDecodeError:
            print("Could not parse important dates JSON")
    
    if weightings_match:
        try:
            weightings = json.loads(weightings_match.group(0))
        except json.JSONDecodeError:
            print("Could not parse weightings JSON")
    
    return important_dates, weightings



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


