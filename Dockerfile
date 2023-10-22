FROM python:3.9

ADD app.py .

RUN pip install streamlit langchain openai chromadb tiktoken pypdf

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
