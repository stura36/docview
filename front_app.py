import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()


st.title("Upload Excel File")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file is not None:
    st.write("File uploaded successfully!")
    # Create a dictionary containing the file and other form data
    files = {
        "file": (
            "uploaded_file.xlsx",
            uploaded_file,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    }

    # Send a POST request to the Flask API
    response = requests.post(os.getenv("BACK_API"), files=files)

    # Display the response from the API
    st.write("API Response:", response.text)
