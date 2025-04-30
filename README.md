---
# Intelligent Resume Parser

A powerful and intelligent resume parsing app that extracts structured data such as name, contact, skills, experience, education, and more from uploaded PDF resumes using OCR and AI (via Together.ai's Mistral model). Built with Python and Streamlit.

---

## Features

- Supports both text-based and scanned (image-based) PDF resumes  
- Uses OCR (Tesseract) to extract text from scanned documents  
- AI-powered parsing using Mistral via Together.ai API  
- Strict JSON schema with confidence scores for each field  
- Post-processing to clean malformed emails and null values  
- Simple Streamlit web interface  

---

## Extracted Fields

The parser returns structured JSON with the following fields:

- `name`  
- `email`  
- `phone`  
- `linkedin`  
- `skills` (list)  
- `education` (degree, institution, year)  
- `experience` (company, title, duration, description)  
- `projects` (title, description)  
- `certifications`  
- `confidence_scores` (for each major section)  

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Intelligent-Resume-Parser.git
cd Intelligent-Resume-Parser
```

### 2. Install Dependencies

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

### 3. Setup Environment Variables

Create a `.env` file in the root directory and add your Together.ai API key:

```env
TOGETHER_API_KEY=your_together_api_key
```

---

### 4. Run the App

```bash
streamlit run main.py
```

Upload a resume PDF in the sidebar and click "Extract Information".

---

## Project Structure

```
.
├── main.py                # Streamlit frontend
├── .env                   # API Key (not tracked by Git)
├── requirements.txt
├── src
│   ├── parser.py          # Calls Together.ai API
│   └── utils.py           # Text extraction & cleaning
└── notebooks
    └── ResumeParser.ipynb # Development notebook
```

---


## Credits

- pdfplumber  
- pytesseract  
- Together.ai  
- Streamlit  

---
