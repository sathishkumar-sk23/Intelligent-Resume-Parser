import streamlit as st
import json
import os
from dotenv import load_dotenv

from src.utils import (
    is_text_based_pdf,
    extract_pdf_text,
    extract_text_from_image_pdf,
    clean_json_output,
    preprocess_ocr
)
from src.parser import call_resume_parser

# Load environment variables
load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

# Streamlit UI setup
st.title("Intelligent Resume Parser")

st.sidebar.header("Upload PDF")
uploaded_file = st.sidebar.file_uploader("Upload your resume in PDF format", type=["pdf"])

if uploaded_file is not None:
    st.sidebar.success("File uploaded successfully!")

    if st.sidebar.button("Extract Information"):
        with st.spinner("Extracting information..."):
            # Check if PDF is text-based or image-based
            is_text_pdf = is_text_based_pdf(uploaded_file)

            if is_text_pdf:
                extracted_text = extract_pdf_text(uploaded_file)
            else:
                extracted_text = extract_text_from_image_pdf(uploaded_file)
                st.text_area("OCR Output1", extracted_text, height=300)
                extracted_text = preprocess_ocr(extracted_text)

            # Call resume parser
            parsed_result = call_resume_parser(extracted_text, api_key)

            # Convert to dictionary and clean null values
            parsed_result = json.loads(parsed_result)
            parsed_result = clean_json_output(parsed_result)
            # print(parsed_result)

        # Display the result
        st.subheader("Extracted Information")
        st.json(parsed_result, expanded=True)

else:
    st.sidebar.info("Please upload a PDF file to proceed.")

