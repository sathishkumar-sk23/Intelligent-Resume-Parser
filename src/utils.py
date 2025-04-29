import pdfplumber

def extract_pdf_text(uploaded_file):
    with pdfplumber.open(uploaded_file) as pdf:
        extracted_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
    return extracted_text
