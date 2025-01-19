import json
from ics import Calendar, Event
from datetime import datetime
import os

def json_to_ics(json_file_path, output_ics_path=None):

    # Check if file exists and is not empty
    if not os.path.exists(json_file_path) or os.path.getsize(json_file_path) == 0:
        print(f"Error: {json_file_path} is empty or does not exist.")
        return None

    # Read the JSON file
    try:
        with open(json_file_path, 'r') as f:
            important_dates = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: Unable to parse JSON from {json_file_path}")
        return None

    # Create a new calendar
    cal = Calendar()
    
    # Process each date entry
    for date_entry in important_dates:
        # Create a new event
        event = Event()
        
        # Set event title
        event.name = date_entry.get('title', 'Untitled Event')
        
        # Parse date and time
        try:
            # Try to parse date with time
            if date_entry.get('time'):
                # Combine date and time
                date_time_str = f"{date_entry['date']} {date_entry['time']}"
                event_datetime = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
            else:
                # If no time, use midnight
                event_datetime = datetime.strptime(date_entry['date'], "%Y-%m-%d")
            
            event.begin = event_datetime
        except (KeyError, ValueError) as e:
            print(f"Could not parse date for {event.name}: {e}")
            continue
    
        # Add event to calendar
        cal.events.add(event)
    
    # If no events were added, return None
    if len(cal.events) == 0:
        print("No valid events found in the JSON file.")
        return None

    # Determine output path
    if output_ics_path is None:
        # Use the same base name as the input JSON file, but with .ics extension
        output_ics_path = os.path.splitext(json_file_path)[0] + '.ics'
    
    # Write calendar to file
    try:
        with open(output_ics_path, 'w') as f:
            f.writelines(cal.serialize_iter())
        
        print(f"ICS file created at: {output_ics_path}")
        return output_ics_path
    except Exception as e:
        print(f"Error writing ICS file: {e}")
        return None