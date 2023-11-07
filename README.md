# Docker Hackathon

Run `pip install -r requirements.txt` to install all dependencies for the project.

To run the app, use `streamlit run app.py`

# Running from Docker

1. Build the image of the file first
`docker build -t pdfreader .`

2. Run the container 
`docker run -p 8501:8501 pdfreader`