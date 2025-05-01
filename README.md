# Intelligent Resume Parser

A powerful AI/NLP-based resume parsing app that extracts structured information from **text-based** PDF resumes using the Mistral model via the Together.ai API. Built with Python and Streamlit.

---

## Features

- Parses **text-based** PDF resumes  
- AI-powered parsing using Mistral via Together.ai API  
- Strict JSON schema with confidence scores for each field  
- Post-processing to clean malformed emails and null values  
- Simple Streamlit web interface  

---

## Extracted Fields

```json
{
  "name": "",
  "email": "",
  "phone": "",
  "linkedin": "",
  "skills": [],
  "education": [
    { "degree": "", "institution": "", "year": "" }
  ],
  "experience": [
    {
      "company": "",
      "title": "",
      "duration": "",
      "description": ""
    }
  ],
  "certifications": [],
  "projects": [],
  "confidence_scores": {
    "name": 0.0,
    "email": 0.0,
    "phone": 0.0,
    "linkedin": 0.0,
    "skills": 0.0,
    "education": 0.0,
    "experience": 0.0,
    "certifications": 0.0,
    "projects": 0.0
  }
}
```

Missing fields return `null`.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Intelligent-Resume-Parser.git
cd Intelligent-Resume-Parser
```

### 2. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 3. Setup Environment Variables

Create a `.env` file:

```env
TOGETHER_API_KEY=your_together_api_key
HUGGINGFACE_API_KEY=your_huggingface_token
```

> **Do not** commit `.env` — add it to `.gitignore`.

### 4. Run the App Locally

```bash
streamlit run main.py
```

Upload a PDF resume through the sidebar and click **Extract Information**.

---

## Project Structure

```
.
├── main.py                # Streamlit frontend
├── requirements.txt
├── .env                   # API Keys (not tracked)
├── src
│   ├── parser.py          # Calls Together.ai API
│   └── utils.py           # PDF text extraction & cleaning
└── sample_resumes/        # Test resume PDFs
```

---

## Tools & Libraries

- **pdfplumber** — text extraction from PDF  
- **Together.ai** (Mistral) — AI parsing API  
- **Streamlit** — web interface  
- **python-dotenv** — environment variable loader  
- **unidecode**, **regex** — text cleaning  

---

## Neurabit Challenge Highlights

- Handles **text-based** PDF resumes  
- Normalizes date formats (e.g., “Jan 2020 – Mar 2022”)  
- Includes **confidence score** (0–1) per field  
- Returns `null` for missing data  

---

## Limitations

- May struggle with **complex layouts** (tables, multi-column text)  
- Extraction quality depends on **resume formatting**  
- Date normalization may require additional edge-case logic  

---

## 🔗 Live Demo

*(Paste your deployed Streamlit URL here once live)*
