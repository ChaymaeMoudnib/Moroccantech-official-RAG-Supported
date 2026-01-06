# MoroccanTech

A web application that provides transparency into the Moroccan tech job market by collecting, analyzing, and visualizing salary and career data from tech professionals across Morocco.

## Overview

MoroccanTech aggregates survey data from tech professionals to create comprehensive visualizations and insights about salaries, career paths, skills, and market trends. The platform helps professionals understand their position in the market and make informed career decisions.

## Features

### Data Visualization
- Real-time data synchronization from Google Sheets
- 30+ interactive visualizations covering demographics, career information, salary analysis, and tech stack usage
- Automatic visualization generation with smart caching
- Background processing for optimal performance

### Resume Analysis
- PDF resume upload and text extraction
- Automatic skill extraction including:
  - Programming languages
  - Cloud services
  - Databases
  - Certifications
- NLP-based entity recognition using spaCy

### RAG-Powered Resume Comparison
- Retrieval-Augmented Generation (RAG) system that compares user resumes with industry-standard position requirements
- Analyzes skill gaps between user profile and typical job requirements
- Provides recommendations for skill development based on market data
- Uses survey data to identify common skill combinations for specific roles
- Generates personalized insights on how user skills align with market expectations

### Salary Transparency
- Salary comparisons by role, experience level, seniority, company type, and location
- Interactive salary distribution charts
- Market positioning analysis

### Data Collection
- Survey participation portal
- Automatic data refresh every 5 minutes
- Google Sheets integration for data management

## Technology Stack

- Backend: FastAPI (Python 3.11.9)
- Data Processing: pandas, NumPy
- Visualizations: Plotly, Matplotlib, Seaborn
- NLP: spaCy, fuzzywuzzy
- Data Source: Google Sheets API (gspread)
- Web Server: Uvicorn
- Templates: Jinja2

## Installation

### Prerequisites
- Python 3.11.9 or compatible version
- Google Sheets API credentials
- spaCy English model


## RAG Resume Comparison Feature

The RAG (Retrieval-Augmented Generation) feature enables intelligent comparison between user resumes and industry-standard position requirements.

### How It Works

1. Resume Analysis: Extracts skills, experience, and qualifications from uploaded resume
2. Position Retrieval: Retrieves relevant position requirements from survey data based on role and seniority level
3. Skill Gap Analysis: Compares user skills against typical requirements for the position
4. Recommendation Generation: Provides actionable insights on:
   - Missing skills that are common in the target position
   - Skill level assessment
   - Career path recommendations
   - Market alignment score

### Usage

Upload a resume through the `/resume` page or use the API endpoint `/upload`. The system will:
- Extract technical skills and certifications
- Compare against market data for similar positions
- Generate a detailed comparison report
- Provide skill development recommendations

## Data Sources

- Google Sheets survey responses
- Real-time data synchronization
- Automatic data refresh every 5 minutes
- Cached visualizations for performance

## Performance Optimizations

- Background visualization generation
- Smart caching based on data hash
- Only regenerates visualizations when data changes
- Async request handling
- Static file serving optimization


## Contact

For questions or support, use the contact form on the website or submit an issue in the repository or contact : chaymaemoudnibe@gmail.com.
