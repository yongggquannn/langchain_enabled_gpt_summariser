# Langchain-Enable-GPT-Summariser

## Project Description: 

The project aims to develop a PDF querying system that leverages LangChain, a powerful language processing tool, to extract information from PDF documents. Users are required to key in their OpenAI API Key to be able to use this PDF Reader. 

## Website
https://langchain-enabled-gpt-summariser-bphxyotpwrirspzh9bodpf.streamlit.app/

## Features:
1. PDF Parsing: The system will use a PDF parsing module to extract text from PDF files, handling various formats, including OCR-processed scanned documents, ensuring thorough data extraction.

2. Langchain Integration: Integration of LangChain, an advanced language tool, will apply techniques like natural language understanding, entity recognition, and contextual comprehension to process text extracted from PDFs.

3. Query Generation: Users will access a user-friendly interface to input search queries, employing diverse parameters like keywords, phrases, date ranges, and document sections for complex queries.

4. Natural Language Processing: LangChain's natural language processing will analyze user queries, identifying relevant context and entities, and then assess PDF content accordingly.

5. Search and Retrieval: Using LangChain's processed data, the system will execute intelligent searches within PDFs, identifying and ranking the most pertinent sections/pages matching user queries for organized retrieval.

6. Data Extraction: Beyond search results, the system will allow specific data extraction from PDFs. Users can set rules based on patterns, keywords, or templates to extract structured data from unstructured PDF content.


## Feasible Use Cases:
1. Academic Research: Researchers and scholars can utilize the system to search for relevant literature, extract citations, or gather information from academic papers saved as PDFs, simplifying the literature review process.

2. Document Management: Organizations can use the system to organize and search through their extensive PDF document repositories, facilitating efficient document retrieval and reducing manual effort.

# Steps to run locally

Run `pip install -r requirements.txt` to install all dependencies for the project.

To run the app, use `streamlit run app.py`

# Running from Docker

1. Build the image of the file first
`docker build -t pdfreader .`

2. Run the container 
`docker run -p 8501:8501 pdfreader`
