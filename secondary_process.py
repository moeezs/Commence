import json
import re

def process_raw_response(response_text):
    """
    Process the raw response text to extract important dates and weightings.
    
    Args:
        response_text (str): Raw text response from Gemini API
    
    Returns:
        tuple: (important_dates, weightings)
    """
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


# Example usage
raw_response_text = """
```json
{
  "important_dates": [
    {
      "title": "First Assignment Due",
      "date": "2025-01-20",
      "time": "23:59:00"
    },
    {
      "title": "Midterm Exam",
      "date": "2025-02-15",
      "time": "10:00:00"
    },
    {
      "title": "Final Exam",
      "date": "2025-04-30",
      "time": "14:00:00"
    }
  ],
  "weightings": [
    {
      "component": "Assignments",
      "weight": "30%"
    },
    {
      "component": "Midterm Exam",
      "weight": "20%"
    },
    {
      "component": "Final Exam",
      "weight": "50%"
    }
  ]
}
```
"""

# Step 1: Process the raw response
# important_dates, weightings = process_raw_response(raw_response_text)

# # Step 2: Save the processed data into separate files
# save_to_files(important_dates, weightings)
