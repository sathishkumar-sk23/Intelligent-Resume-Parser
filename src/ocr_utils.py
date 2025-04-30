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
                extracted_text = preprocess_ocr(extracted_text)

            # Call resume parser
            parsed_result = call_resume_parser(extracted_text, api_key)

            # Convert to dictionary and clean null values
            parsed_result = json.loads(parsed_result)
            parsed_result = clean_json_output(parsed_result)
            print(parsed_result)

        # Display the result
        st.subheader("Extracted Information")
        st.json(parsed_result, expanded=True)

else:
    st.sidebar.info("Please upload a PDF file to proceed.")








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
st.set_page_config(page_title="Intelligent Resume Parser", layout="wide")
st.title("Intelligent Resume Parser")
st.markdown("Upload a resume in PDF format, and this app will extract structured information using OCR + AI.")

st.sidebar.header("Upload PDF")
uploaded_file = st.sidebar.file_uploader("Upload your resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    st.sidebar.success("File uploaded successfully!")

    if st.sidebar.button("Extract Information"):
        with st.spinner("Processing resume..."):
            try:
                # Step 1: Detect PDF type
                is_text_pdf = is_text_based_pdf(uploaded_file)

                # Step 2: Extract text
                if is_text_pdf:
                    raw_text = extract_pdf_text(uploaded_file)
                else:
                    raw_text = extract_text_from_image_pdf(uploaded_file)
                    raw_text = preprocess_ocr(raw_text)

                if not raw_text.strip():
                    st.error("Failed to extract any text from the PDF.")
                    st.stop()

                # Step 3: Call resume parser
                llm_response = call_resume_parser(raw_text, api_key)

                try:
                    parsed_result = json.loads(llm_response)
                except json.JSONDecodeError as e:
                    st.error("Failed to parse LLM response as JSON.")
                    st.text(llm_response)  # Show raw text for debugging
                    st.stop()

                # Step 4: Clean parsed output
                parsed_result = clean_json_output(parsed_result)

                # Step 5: Show results
                st.subheader("Extracted Information")
                st.json(parsed_result, expanded=True)

            except Exception as e:
                st.error(f" Something went wrong: {e}")

else:
    st.sidebar.info("Please upload a PDF file to proceed.")
