import os
from apikey import apikey

import streamlit as st
from langchain.llms import openai

from langchain.document_loaders import PyPDFLoader

os.environ['OPENAI_API_KEY'] = apikey

#App framework
st.title('🐳 LLM-Powered PDF Summarizer')



