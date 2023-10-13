import os
from apikey import apikey

import streamlit as st
from langchain.llms import openai

os.environ['OPENAI_API_KEY'] = apikey

#App framework
st.title('🐳 Docker Product Queries')
prompt = st.text_input('Plug in your prompt here')
