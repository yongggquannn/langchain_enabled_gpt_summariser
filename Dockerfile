FROM python:3.9

ADD app.py .

RUN pip install streamlit pypdf2 langchain python-dotenv faiss-cpu openai huggingface_hub

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
