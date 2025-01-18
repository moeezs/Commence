from flask import Flask, render_template, request, send_file
import os
# from gemini import printout

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def upload_file():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return 'No file uploaded', 400
    
    pdf_file = request.files['pdf_file']
    if pdf_file.filename == '':
        return 'No selected file', 400
    
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
    pdf_file.save(pdf_path)
    
    extracted_text = 'hello'#printout(pdf_path)

    # Optional: Save extracted text to a file if needed
    # text_output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'extracted_text.txt')
    # with open(text_output_path, 'w') as f:
    #     f.write(extracted_text)
    
    # Generate ICS file
    ics_path = 'important_dates.ics' #json_to_ics('important_dates.json')
    
    return render_template('upload.html', extracted_text=extracted_text, ics_available=ics_path is not None)

@app.route('/download_ics')
def download_ics():
    ics_path = 'important_dates.ics'
    try:
        return send_file(ics_path, as_attachment=True, download_name='important_dates.ics')
    except FileNotFoundError:
        return 'ICS file not found', 404


if __name__ == '__main__':
    app.run(debug=True)