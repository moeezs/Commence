from gemini_send import analyze_syllabus
from pdf_processor import extract_pdf_text
from secondary_process import process_raw_response, save_to_files
from json_ics import json_to_ics

pdf_text = extract_pdf_text('syllabus.pdf')


jsons = analyze_syllabus(pdf_text)

print(jsons)

important_dates, weightings = process_raw_response(jsons)
save_to_files(important_dates, weightings)

json_to_ics('important_dates.json')

# a file is saved in this directory as important_dates.json, course_weightings.json, important_dates.ics