import pdfplumber
import os
import spacy
from spacy.matcher import PhraseMatcher
from fuzzywuzzy import fuzz

nlp = spacy.load("en_core_web_sm")

programming_languages = ["python", "r", "java", "c++", "javascript", "sql", "go", "ruby", "html", "css", "php"]
cloud_services = ["aws", "azure", "google cloud", "ibm cloud", "oracle cloud"]
databases = ["mysql", "mongodb", "postgresql", "sqlite", "redis"]
certifications = [
    "aws certified", "google cloud certified", "microsoft certified", "pmp", "scrum master",
    "data scientist certification", "ai certification", "python programmer bootcamp", "web scraping"
]
keywords = programming_languages + cloud_services + databases + certifications

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
patterns = [nlp.make_doc(keyword) for keyword in keywords]
matcher.add("TECH_SKILLS", patterns)

def save_uploaded_file(file, upload_folder="uploads"):
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)
    try:
        file.save(file_path)
        print(f"[INFO] File saved at {file_path}")
        return file_path
    except Exception as e:
        print(f"[ERROR] File save failed: {e}")
        return None

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"[ERROR] Failed to extract text from {pdf_path}: {e}")
        return None
    return text.strip()

def extract_entities(text):
    doc = nlp(text.lower())  # Normalize text to lowercase
    matches = matcher(doc)
    
    extracted_data = {
        "programming_languages": set(),
        "cloud_services": set(),
        "databases": set(),
        "certifications": set(),
    }

    # Extract exact matches
    for match_id, start, end in matches:
        keyword = doc[start:end].text
        if keyword in programming_languages:
            extracted_data["programming_languages"].add(keyword)
        elif keyword in cloud_services:
            extracted_data["cloud_services"].add(keyword)
        elif keyword in databases:
            extracted_data["databases"].add(keyword)
        elif keyword in certifications:
            extracted_data["certifications"].add(keyword)

    for keyword in keywords:
            for token in doc:
                if fuzz.partial_ratio(token.text, keyword) >= 80:
                    if keyword in programming_languages:
                    extracted_data["programming_languages"].add(keyword)
                elif keyword in cloud_services:
                    extracted_data["cloud_services"].add(keyword)
                elif keyword in databases:
                    extracted_data["databases"].add(keyword)
                elif keyword in certifications:
                    extracted_data["certifications"].add(keyword)

    # Fuzzy matching with broader terms for certifications and training
    broader_terms = {
        "programming_languages": ["py", "js", "sql", "java", "csharp", "c", "ruby"],
        "cloud_services": ["cloud"],
        "databases": ["db", "database"],
        "certifications": ["cert", "certificate", "certification", "training", "bootcamp", "ai training"],
    }

    for category, terms in broader_terms.items():
        for term in terms:
            for token in doc:
                if fuzz.partial_ratio(token.text, term) >= 80:
                    extracted_data[category].add(term)

    return {key: list(value) for key, value in extracted_data.items()}
