from flask import Flask, render_template, request, jsonify, send_file
import os
import pdfplumber
from fpdf import FPDF
import requests
import json
from dotenv import load_dotenv

load_dotenv()  # Load the .env file

api_key = os.getenv("My_Api_Key")


app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

My_Api_Key = "Bearer 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"

@app.route('/')
def index():
    for file in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, file)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
    
    return render_template("index.html")



@app.route('/upload', methods=['POST'])
def upload_file():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['pdf']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Extract text after saving the file
        extracted_text = extract_text_from_pdf(file_path)

        if not extracted_text.strip():  # If no text is extracted
            os.remove(file_path)  # Delete unusable file
            return jsonify({'error': '❌ Unable to extract text from this PDF. Try another file.'}), 400

        # Store extracted text in a file
        with open("extracted_text.txt", "w", encoding="utf-8") as f:
            f.write(extracted_text)

        return jsonify({'message': 'File uploaded successfully!'}), 200

    return jsonify({'error': 'Invalid file type. Only PDFs allowed.'}), 400


def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        return f"Error extracting text: {str(e)}"

@app.route('/generate', methods=['POST'])
def generate_questions():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid JSON input'}), 400

        question_type = data.get("questionType", "MCQ")
        difficulty = data.get("difficulty", "Medium")
        text_input = data.get("textInput", "").strip()

        extracted_text = ""
        if os.path.exists("extracted_text.txt"):
            with open("extracted_text.txt", "r", encoding="utf-8") as f:
                extracted_text = f.read().strip()

        # Choose the input source: user text or extracted PDF text
        final_text = text_input if text_input else extracted_text
        if not final_text:
            return jsonify({'error': 'No valid text input found'}), 400

        # Generate questions based on the text
        request_payload = {
            "model": "google/gemini-2.0-flash-thinking-exp:free",
            "messages": [
                {
                    "role": "user",
                    "content": f"Based on the following text, generate 15 {difficulty} level {question_type} questions. Do not give answer or explanation. No extra *#etc just plain text. There should be question no. before every question. Make sure the type of questions is {question_type}:\n\n{final_text}"
                }
            ]
        }

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": My_Api_key,
                "Content-Type": "application/json"
            },
            json=request_payload
        )

        response.raise_for_status()
        api_response = response.json()
        questions = api_response.get("choices", [])[0].get("message", {}).get("content", "").strip().split('\n')

        # Save generated questions to a file
        with open("generated_questions.txt", "w", encoding="utf-8") as f:
            for question in questions:
                f.write(question + "\n")

        # Generate a PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        for question in questions:
            pdf.multi_cell(0, 10, question)

        pdf.output("generated_questions.pdf")

        return jsonify({'message': 'Questions generated successfully!', 'questions': questions})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Failed to fetch questions', 'details': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'details': str(e)}), 500


@app.route('/output')
def output_page():
    questions = []
    try:
        with open("generated_questions.txt", "r", encoding="utf-8") as f:
            questions = f.readlines()
    except FileNotFoundError:
        questions = ["No questions generated yet."]
    return render_template('output.html', questions=[q.strip() for q in questions])

@app.route('/download', methods=['GET'])
def download_pdf():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    try:
        with open("generated_questions.txt", "r", encoding="utf-8") as f:
            questions = f.readlines()
    except FileNotFoundError:
        questions = ["No questions generated."]

    for question in questions:
        pdf.multi_cell(0, 10, question.strip())

    pdf_filename = "generated_questions.pdf"
    pdf.output(pdf_filename)

    return send_file(pdf_filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
