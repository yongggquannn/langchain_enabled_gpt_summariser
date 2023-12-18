import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmltemplates import css, bot_template, user_template
import langcheck
import io
import os
import openai

# Method to check if API key is valid
def check_api_key(api_key):
    openai.api_key = api_key
    try:
        openai.Model.list()
    except openai.error.AuthenticationError as e:
        return False
    else:
        return True

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(io.BytesIO(pdf.read()))
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(text_chunks, embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI()
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    # Reverse chat history in order to display latest query at the top
    reversed_chat_history = reversed(st.session_state.chat_history)

    if reversed_chat_history:  # Check if the list is not empty
        for i, message in enumerate(reversed_chat_history):
            if i % 2 == 0:
                st.write(user_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
            else:
                st.write(bot_template.replace(
                    "{{MSG}}", message.content), unsafe_allow_html=True)
                
    return st.session_state.chat_history



def main():
    st.set_page_config(page_title="GPT Summariser", page_icon=":whale:")
    st.write(css, unsafe_allow_html=True)

    # Initialise as empty string and update whenever files are processed
    source_text = "" 

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("LangChain-enabled GPT Summariser :whale:")

    # Create a placeholder for the input field
    api_key_placeholder = st.empty()

    # Input field for OpenAI API key
    api_key = api_key_placeholder.text_input("Enter your OpenAI API Key:")

    # Check if API key has been entered
    if api_key:
        if check_api_key(api_key):
            # Clear the input field
            api_key_placeholder.empty()

            # Set the API key in the environment variables
            os.environ["OPENAI_API_KEY"] = api_key

            user_question = st.text_input("Ask a question about your documents:")
            submit_button = st.button("Submit")

            if submit_button:
                # Retrieving AI answer
                queries_answers = handle_user_input(user_question)
                ai_answer = queries_answers[-1].content

                # # Adding fluency score into main 
                # fluency_score = langcheck.metrics.fluency(ai_answer).metric_values[0]

                # # Adding factual consistency score
                # factual_consistency_score = langcheck.metrics.en.source_based_text_quality.factual_consistency(generated_outputs= ai_answer,
                #                                                                                                 sources = source_text,
                #                                                                                                 prompts= user_question,
                #                                                                                                 model_type= 'local').metric_values[0]

                # st.markdown(f"""
                #     <strong style="font-size: 20px; color: white;">This answer has a fluency score of: {fluency_score}</strong><br>
                #     <strong style="font-size: 20px; color: white;">This answer has an accuracy score of: {factual_consistency_score}</strong>
                # """, unsafe_allow_html=True)
        # Invalid API key
        elif not check_api_key(api_key):
            st.error("Invalid API Key")
    


    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDF here and click on 'Process' (Limited to one PDF)", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing..."):
                # get pdf text
                raw_text = get_pdf_text(pdf_docs)
                source_text = raw_text

                # get the text chunks
                text_chunks = get_text_chunks(raw_text)

                # create vector store
                vectorstore = get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)


if __name__ == '__main__':
    main()