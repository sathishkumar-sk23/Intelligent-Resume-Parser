import pdfplumber
from pdf2image import convert_from_bytes
import pytesseract
from io import BytesIO
import re

# ----------------------- PDF Type Detection -----------------------

def is_text_based_pdf(pdf_path):
    """
    Check if a PDF is text-based (as opposed to scanned image-based).
    Args:
        pdf_path (str or file-like): Path to the PDF or uploaded file.
    Returns:
        bool: True if the PDF contains extractable text, False if it's image-based.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text and text.strip():
                    return True
        return False
    except Exception as e:
        print(f"[PDF CHECK ERROR] Failed to determine PDF type: {e}")
        return False


# ----------------------- Text Extraction -----------------------

def extract_pdf_text(uploaded_file):
    """
    Extract raw text from a text-based PDF using pdfplumber.
    Args:
        uploaded_file (file-like): PDF file uploaded by the user.
    Returns:
        str: Concatenated text from all PDF pages.
    """
    extracted_text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"
        return extracted_text.strip()
    except Exception as e:
        print(f"[PDFPLUMBER ERROR] Failed to extract text: {e}")
        return ""


def extract_text_from_image_pdf(pdf_bytes):
    try:
        from pdf2image import convert_from_bytes
        from pytesseract import image_to_string

        # wrap bytes in BytesIO to make it a file-like object
        from io import BytesIO
        pdf_file = BytesIO(pdf_bytes)

        images = convert_from_bytes(pdf_file.read())
        text = ""
        for image in images:
            text += image_to_string(image)
        return text

    except Exception as e:
        print(f"[OCR ERROR] Failed to extract text from image PDF: {e}")
        return ""



# ----------------------- Text Cleaning -----------------------

def preprocess_ocr(text):
    """
    Clean raw OCR output text (remove non-ASCII, special characters).
    Args:
        text (str): Raw OCR text.
    Returns:
        str: Cleaned and normalized text.
    """
    if not text:
        return ""

    text = re.sub(r"[^\x00-\x7F]+", "", text)      # Remove non-ASCII
    text = re.sub(r"[&*@#€¢•¶]+", "", text)         # Remove OCR junk
    return text.strip()


# ----------------------- JSON Cleanup -----------------------

def fix_email(email):
    """
    Attempt to fix common malformed emails from OCR (e.g., missing '@').
    """
    if isinstance(email, str) and email and "@" not in email:
        match = re.search(r"(\w+)(gmail|yahoo|outlook|protonmail|hotmail)\.com", email)
        if match:
            corrected = match.group(1) + "@" + match.group(2) + ".com"
            return corrected
    return email


def clean_json_output(parsed_output):
    """
    Cleans the parsed JSON output by replacing string "null" with None,
    and applies email fixing logic where necessary.
    """
    if isinstance(parsed_output, dict):
        for key, value in parsed_output.items():
            if isinstance(value, dict):
                parsed_output[key] = clean_json_output(value)
            elif isinstance(value, list):
                for i in range(len(value)):
                    if isinstance(value[i], dict):
                        value[i] = clean_json_output(value[i])
                    elif value[i] == "null":
                        value[i] = None
            elif value == "null":
                parsed_output[key] = None

            if key == "email":
                parsed_output[key] = fix_email(value)

    return parsed_output
