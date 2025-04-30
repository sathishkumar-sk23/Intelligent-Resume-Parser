import requests
import json

def call_resume_parser(cleaned_text: str, api_key: str) -> dict:
    """
    Call the resume parser API with the cleaned text and return the structured JSON response.
    
    """

    prompt = f"""
    You are an expert resume parser.

    Task:
    Parse the following resume content and extract structured fields. Return the result ONLY in the following strict JSON format:

    Instructions:
    - Do not guess. If a field is not explicitly present in the text, set its value to the JSON null value (without quotes).
    - Read the ENTIRE content carefully, especially the profile/summary and projects section, to extract all relevant skills.
    - Add skills from projects or summary sections **only if they are not already included** in the skills list.
    - LinkedIn:
        1. Only extract a LinkedIn URL if it's a valid personal profile starting with:
            "https://linkedin.com/in/" or "https://www.linkedin.com/in/".
        2. If the resume contains a general LinkedIn link like "linkedin.com" or just the word "LinkedIn" without a full URL, return null.
        3. Do not guess or generate a LinkedIn URL based on name.
    - Work Experience vs. Projects:
        1. Treat as **work experience** only if BOTH a valid company name and a clear duration (e.g., "Jan 2020 – Mar 2022") are present.
        2. If any of the following are **missing** — company name, duration, or job title — classify it as a **project**.
        3. Terms like "Project", "Capstone", "Intern Project", "Practical Experience", or job simulation **should be treated as projects**, NOT experience.
        4. Extract project title and description from such entries and move them to the "projects" section.
    - Normalize all dates to "MMM YYYY" format where possible (e.g., "Jan 2020").
    - Include a confidence score (0.0–1.0) for each field in the `confidence_scores` section.
    - Return all results ONLY in this strict JSON format:

    {{
    "name": "",
    "email": "",
    "phone": "",
    "linkedin": "",
    "skills": [],
    "education": [
        {{
        "degree": "",
        "institution": "",
        "year": ""
        }}
    ],
    "experience": [
        {{
        "company": "",
        "title": "",
        "duration": "",
        "description": ""
        }}
    ],
    "certifications": [],
    "projects": [
        {{
        "title": "",
        "description": ""
        }}
    ],
    "confidence_scores": {{
        "name": 0.0,
        "email": 0.0,
        "phone": 0.0,
        "linkedin": 0.0,
        "skills": 0.0,
        "education": 0.0,
        "experience": 0.0,
        "certifications": 0.0,
        "projects": 0.0
    }}
    }}

    Text to extract from:
    \"\"\"
    {cleaned_text}
    \"\"\"
    """

    response = requests.post(
        "https://api.together.xyz/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": "mistralai/Mistral-7B-Instruct-v0.2",
            "messages": [
                {"role": "system", "content": "You are an expert in reading resumes."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "top_p": 0.9,
            "max_tokens": 2048,
        }
    )

    response.raise_for_status()
    output = response.json()
    return output["choices"][0]["message"]["content"]
