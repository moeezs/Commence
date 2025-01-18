from flask import Flask, render_template, request, jsonify, send_file, Response, session
import json
import os
from werkzeug.utils import secure_filename
from gemini_send import analyze_syllabus
from pdf_processor import extract_pdf_text
from secondary_process import process_raw_response, save_to_files
from json_ics import json_to_ics
import time
import uuid
from datetime import timedelta
import secrets
from dotenv import load_dotenv

load_dotenv()

# Generate a persistent secret key
SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
print(SECRET_KEY)
if not SECRET_KEY:
    SECRET_KEY = secrets.token_hex(16)
    # Optionally, save this to .env for persistence
    with open('.env', 'a') as f:
        f.write(f'\nFLASK_SECRET_KEY={SECRET_KEY}')

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.permanent_session_lifetime = timedelta(days=30)  # Session lasts 30 days

# Configure file storage
UPLOAD_FOLDER = 'user_data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# def get_user_folder():
#     """Get or create user-specific folder"""
#     if 'user_id' not in session:
#         session.permanent = True
#         session['user_id'] = str(uuid.uuid4())
#         session['courses'] = []  # Initialize courses list in session
    
#     user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['user_id'])
#     os.makedirs(user_folder, exist_ok=True)
#     return user_folder

def get_user_folder():
    """Get or create user-specific folder"""
    # Check if user_id already exists in session
    if 'user_id' not in session:
        session.permanent = True
        # Try to get user_id from environment or generate a new one
        stored_user_id = os.getenv('PERSISTENT_USER_ID')
        if not stored_user_id:
            stored_user_id = str(uuid.uuid4())
            # Save to .env to persist across sessions
            with open('.env', 'a') as f:
                f.write(f'\nPERSISTENT_USER_ID={stored_user_id}')
        
        session['user_id'] = stored_user_id
        
        # Initialize courses list if not exists
        if 'courses' not in session:
            session['courses'] = []
    
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], session['user_id'])
    os.makedirs(user_folder, exist_ok=True)
    return user_folder

def process_weightings(weightings):
    """Process weightings to extract component and weight values"""
    processed = []
    if isinstance(weightings, list):
        for item in weightings:
            if isinstance(item, dict):
                component = item.get('component', '')
                weight = item.get('weight', '0')
                if isinstance(weight, str):
                    weight = weight.replace('%', '')
                if component and weight:
                    processed.append({
                        'component': component,
                        'weight': weight
                    })
    return processed

@app.route('/')
def index():
    get_user_folder()
    return render_template('index.html', courses=session.get('courses', []))

@app.route('/api/upload', methods=['POST'])
def upload_file():
    session.permanent = True
    if 'syllabus' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['syllabus']
    course_name = request.form.get('courseName', '')
    secure_course_name = secure_filename(course_name)
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        user_folder = get_user_folder()
        filename = secure_filename(file.filename)
        filepath = os.path.join(user_folder, filename)
        file.save(filepath)
        
        try:
            pdf_text = extract_pdf_text(filepath)
            jsons = analyze_syllabus(pdf_text)
            important_dates, weightings = process_raw_response(jsons)
            
            # Save files in user's folder
            dates_json = os.path.join(user_folder, f'important_dates_{secure_course_name}.json')
            weights_json = os.path.join(user_folder, f'course_weightings_{secure_course_name}.json')
            
            # Save files directly to user folder
            with open(dates_json, 'w') as f:
                json.dump(important_dates, f)
            with open(weights_json, 'w') as f:
                json.dump(weightings, f)
            
            # Generate ICS file in user folder
            ics_file = os.path.join(user_folder, f'important_dates_{secure_course_name}.ics')
            json_to_ics(dates_json, output_ics_path=ics_file)
            
            time.sleep(2)
            
            with open(weights_json, 'r') as f:
                weightings_data = json.load(f)
                processed_weightings = process_weightings(weightings_data)
            
            # Update session data
            courses = session.get('courses', [])
            course_data = {
                'name': course_name,
                'weightings': processed_weightings
            }
            courses.append(course_data)
            session['courses'] = courses
            
            return jsonify({
                'success': True,
                'courseName': course_name,
                'weightings': processed_weightings
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)

@app.route('/api/calendar/<course_name>')
def download_calendar(course_name):
    try:
        user_folder = get_user_folder()
        base_name = secure_filename(course_name)
        ics_file = os.path.join(user_folder, f'important_dates_{base_name}.ics')
        
        return send_file(
            ics_file,
            mimetype='text/calendar',
            as_attachment=True,
            download_name=f'{course_name}_calendar.ics'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)