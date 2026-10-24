# HireSense — Recruitment Intelligence & Applicant Tracking System

## Overview
HireSense is a recruitment workflow management web application designed to help recruiters organize job openings, manage candidate information, and compare candidate skills against job requirements.

This project was developed as an educational portfolio MVP using Python, FastAPI, SQLite, HTML, CSS, and JavaScript.

## Key Features
- **Job Management:** Create and view job openings.
- **Candidate Management:** Add and view candidate profiles.
- **Candidate Matching:** Calculate an explainable match score using required skills (80%) and experience alignment (20%).
- **Skill Gap Analysis:** Identify matching and missing skills for each candidate.
- **Recruitment Pipeline:** Track candidates through Applied, Shortlisted, Interview, Selected, and Rejected stages.
- **Dashboard:** View recruitment summary metrics.
- **Data Persistence:** Store project data using SQLite.
- **Responsive Interface:** Access the dashboard through a web browser.

## Technology Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python, FastAPI
- Database: SQLite
- API Documentation: FastAPI Swagger UI

## Installation and Setup

### Prerequisites
- Python 3.10 or later
- pip

### Run on Windows
```powershell
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Access the Application
- Web application: http://127.0.0.1:8000
- API documentation: http://127.0.0.1:8000/docs

## Project Structure
```text
HireSense-Original/
├── app/
│   ├── main.py
│   └── static/
│       ├── index.html
│       ├── style.css
│       └── app.js
├── requirements.txt
├── .gitignore
└── README.md
```

## Use Case
HireSense demonstrates how a recruitment team can manage job openings, review candidates, compare skills, and track recruitment progress in one place.

## Limitations
This is an educational MVP and does not include authentication or production-grade access controls. Match scores are estimates intended to support human review, not replace recruiter decisions. The application uses fictional demonstration data; do not enter real candidate personal information.

## Future Enhancements
- Secure login and role-based access
- Resume upload and parsing
- Email notifications for interview updates
- Advanced reporting and analytics
- Integration with external recruitment platforms
