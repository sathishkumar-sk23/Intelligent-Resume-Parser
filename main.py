import streamlit as st


from dotenv import load_dotenv
import os
from src.utils import extract_pdf_text
from src.parser import call_resume_parser

load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")


st.title("Intelligent Resume Parser")

st.sidebar.header("Upload PDF")
uploaded_file = st.sidebar.file_uploader("Upload your resume in PDF format", type=["pdf"])

if uploaded_file is not None:
    st.sidebar.success("File uploaded successfully!")
    if st.sidebar.button("Extract Information"):
        with st.spinner("Extracting information..."):
            extracted_text = pdf_text = extract_pdf_text(uploaded_file)
            # Call Mistral
            parsed_result = call_resume_parser(extracted_text, api_key)
        st.subheader("Extracted Information")
        st.text_area("Resume Content", parsed_result, height=400)
else:
    st.sidebar.info("Please upload a PDF file to proceed.")
