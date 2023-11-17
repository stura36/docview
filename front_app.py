import streamlit as st
import requests
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()


st.title("Upload Document Data")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file is not None:
    files = {
        "file": (
            "uploaded_file.xlsx",
            uploaded_file,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    }
    if st.button("Send"):
        response = requests.post(os.getenv("BACK_API"), files=files)
        st.success("File sent successfully!")
        st.write("API Response:", response.text)
    st.subheader("Data preview")
    df = pd.read_excel(uploaded_file)
    st.dataframe(df.head())
