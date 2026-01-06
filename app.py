from flask import Flask, render_template, request,jsonify,redirect, url_for, session
from Features.part1 import visualize_gender,visualize_age,visualize_diploma,visualize_diploma2,visualize_diploma_clusters
from Features.part2 import visualize_role,visualize_experience,visualize_seniorit,visualize_company_size,visualize_company_type,visualize_sectors,visualize_sector_2,visualize_work_mode
from Features.part3 import visualize_salary_satisfaction_by_gender,visualize_bonus_frequency_by_seniority
from Features.part4 import visualize_cloud_services_usage,visualize_daily_work_tools,visualize_certifications,visualize_database_usage,visualize_programming_languages,visualize_company_name_sharing

from Features.salary import visualize_salary_by_gender,visualize_salary_by_company_type,visualize_salary_by_work_mode,visualize_salary_by_role,visualize_salary_by_seniority,visualize_salary_by_experience,visualize_salary_by_age,visualize_salary_by_diploma
import json
import os
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import re
from flask_cors import CORS
from dotenv import load_dotenv
import threading
import time
from google.oauth2.service_account import Credentials



load_dotenv()

app = Flask(__name__)
CORS(app)

if os.getenv('RENDER') is not None: 
    CREDS_FILE = '/etc/secrets/credentials.json' 
else:
    CREDS_FILE = 'C:/Users/user/Documents/Projects/MoroccanTech/credentials.json'  # Path for local testing

if CREDS_FILE is None:
    raise ValueError("The CREDENTIALS_JSON environment variable is not set.")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)

SHEET_ID = "1RFwkEoUDpQ_rcSaN_n1i6S_UaiSsubakIyUmkLXwdUM"
WORKSHEET_NAME = "Réponses au formulaire 1"

# ✅ Load initial data before anything else
def fetch_latest_data():
    """Fetch the latest data from Google Sheets."""
    sheet = gc.open_by_key(SHEET_ID)
    worksheet = sheet.worksheet(WORKSHEET_NAME)
    data = worksheet.get_all_records()
    return pd.DataFrame(data)  

df = fetch_latest_data()

def auto_refresh(interval=30):
    """Refresh the DataFrame every `interval` seconds."""
    global df
    while True:
        try:
            df = fetch_latest_data()  
            print("✅ Data updated successfully.")
        except Exception as e:
            print(f"⚠️ Error updating data: {e}")
        time.sleep(interval)  # Wait before refreshing again

thread = threading.Thread(target=auto_refresh, daemon=True)
thread.start()

@app.route('/get_data', methods=['GET'])
def get_data():
    """API endpoint to return the latest data."""
    return jsonify(df.to_dict(orient='records'))

# print(df)


visualize_gender(df)
visualize_age(df)
visualize_diploma(df)
visualize_diploma2(df)
visualize_diploma_clusters(df)


visualize_role(df)
visualize_experience(df)
visualize_seniorit(df)
visualize_sectors(df)
visualize_sector_2(df)
visualize_work_mode(df)
visualize_company_type(df)
visualize_company_size(df)
visualize_company_name_sharing(df)
visualize_programming_languages(df)
visualize_database_usage(df)
visualize_cloud_services_usage(df)
visualize_certifications(df)
visualize_daily_work_tools(df)

visualize_bonus_frequency_by_seniority(df)
visualize_salary_satisfaction_by_gender(df)

visualize_salary_by_gender(df)
visualize_salary_by_company_type(df)
visualize_salary_by_work_mode(df)
visualize_salary_by_role(df)
visualize_salary_by_diploma(df)
visualize_salary_by_seniority(df)
visualize_salary_by_experience(df)
visualize_salary_by_age(df)

# generate_salary_dis_visualizations(df)

@app.route("/report")
def report():
    
    return render_template("report.html")


def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')    
    return jsonify({'status': 'success', 'message': 'Email sent successfully!'})
    
@app.route("/participate")
def par():
    return render_template("participate.html")


@app.route("/compare2")
def compare2():
    return render_template("Compare.html")
# app.register_blueprint(comp_bp)
@app.route("/test")
def test():
    return render_template("test.html")

@app.route("/resume")
def resume():
    return render_template("resume.html")

@app.route("/compare3")
def compare3():
    return render_template("compare1.html")


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    file_path = save_uploaded_file(file)
    if not file_path:
        return jsonify({"error": "Failed to save the file"}), 500
    resume_text = extract_text_from_pdf(file_path)
    if not resume_text:
        return jsonify({"error": "Failed to extract text from the resume"}), 500
    extracted_entities = extract_entities(resume_text)
    return jsonify({
        "resume_text": resume_text,
        "entities": extracted_entities
    })

@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8030, debug=True)