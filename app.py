import os
from apikey import apikey

import streamlit as st
from langchain.llms import OpenAI

from langchain.document_loaders import PyPDFLoader

os.environ['OPENAI_API_KEY'] = apikey

#App framework
st.set_page_config(page_title="SummarizerGPT", page_icon="📖", layout="wide")
st.header("📖 SummarizerGPT")

llm = OpenAI(temperature = 0.9)

uploaded_file = st.file_uploader(
    "Upload a pdf, docx, or txt file",
    type=["pdf", "docx", "txt"],
    help="Scanned documents are not supported yet!",
)


