from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
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
from dotenv import load_dotenv
import threading
import time
import hashlib
from google.oauth2.service_account import Credentials

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

if os.getenv('RENDER') is not None: 
    CREDS_FILE = '/etc/secrets/credentials.json' 
else:
    CREDS_FILE = 'C:/Users/user/OneDrive/Documents/Projects_c/MoroccanTech/credentials.json'

if CREDS_FILE is None:
    raise ValueError("The CREDENTIALS_JSON environment variable is not set.")

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
gc = gspread.authorize(creds)

SHEET_ID = "1RFwkEoUDpQ_rcSaN_n1i6S_UaiSsubakIyUmkLXwdUM"
WORKSHEET_NAME = "Réponses au formulaire 1"

CACHE_FILE = 'static/Images/.data_hash.txt'

def get_data_hash(df):
    """Generate hash of DataFrame to detect changes."""
    return hashlib.md5(pd.util.hash_pandas_object(df).values.tobytes()).hexdigest()

def fetch_latest_data():
    """Fetch the latest data from Google Sheets."""
    sheet = gc.open_by_key(SHEET_ID)
    worksheet = sheet.worksheet(WORKSHEET_NAME)
    data = worksheet.get_all_records()
    return pd.DataFrame(data)  

def generate_all_visualizations(df):
    """Generate all visualizations - runs in background thread."""
    try:
        print(" Starting visualization generation...")
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
        
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, 'w') as f:
            f.write(get_data_hash(df))
        print("All visualizations generated successfully!")
    except Exception as e:
        print(f"Error generating visualizations: {e}")

def should_regenerate_visualizations(df):
    """Check if visualizations need to be regenerated."""
    current_hash = get_data_hash(df)
    if not os.path.exists(CACHE_FILE):
        return True
    try:
        with open(CACHE_FILE, 'r') as f:
            cached_hash = f.read().strip()
        return cached_hash != current_hash
    except:
        return True

df = fetch_latest_data()

def auto_refresh(interval=300):
    """Refresh data and regenerate visualizations if needed."""
    global df
    while True:
        try:
            new_df = fetch_latest_data()
            if not df.equals(new_df) or should_regenerate_visualizations(new_df):
                df = new_df
                print(" Data changed, regenerating visualizations...")
                generate_all_visualizations(df)
            else:
                df = new_df
                print(" Data checked, no changes detected.")
        except Exception as e:
            print(f"Error updating data: {e}")
        time.sleep(interval)

if should_regenerate_visualizations(df):
    print("Generating initial visualizations in background...")
    viz_thread = threading.Thread(target=generate_all_visualizations, args=(df,), daemon=True)
    viz_thread.start()
else:
    print(" Visualizations are up to date, skipping generation.")

refresh_thread = threading.Thread(target=auto_refresh, daemon=True)
refresh_thread.start()

@app.get('/get_data')
async def get_data():
    """API endpoint to return the latest data."""
    return df.to_dict(orient='records')

@app.post('/regenerate_viz')
async def regenerate_viz():
    """Manually trigger visualization regeneration."""
    global df
    try:
        df = fetch_latest_data()
        generate_all_visualizations(df)
        return {'status': 'success', 'message': 'Visualizations regenerated!'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report", response_class=HTMLResponse)
async def report(request: Request):
    return templates.TemplateResponse("report.html", {"request": request})

def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

@app.post('/contact')
async def contact(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    return {'status': 'success', 'message': 'Email sent successfully!'}
    
@app.get("/participate", response_class=HTMLResponse)
async def par(request: Request):
    return templates.TemplateResponse("participate.html", {"request": request})

@app.get("/compare2", response_class=HTMLResponse)
async def compare2(request: Request):
    return templates.TemplateResponse("Compare.html", {"request": request})

@app.get("/test", response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

@app.get("/resume", response_class=HTMLResponse)
async def resume(request: Request):
    return templates.TemplateResponse("resume.html", {"request": request})

@app.get("/compare3", response_class=HTMLResponse)
async def compare3(request: Request):
    return templates.TemplateResponse("compare1.html", {"request": request})

@app.post('/upload')
async def upload_file(file: UploadFile = File(...)):
    from Features.resume import save_uploaded_file, extract_text_from_pdf, extract_entities
    if not file.filename:
        raise HTTPException(status_code=400, detail="No selected file")
    
    upload_folder = "uploads"
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)
    
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save the file: {str(e)}")
    
    resume_text = extract_text_from_pdf(file_path)
    if not resume_text:
        raise HTTPException(status_code=500, detail="Failed to extract text from the resume")
    
    extracted_entities = extract_entities(resume_text)
    return {
        "resume_text": resume_text,
        "entities": extracted_entities
    }

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8030)