import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ChatMessageHistory
from langchain.chains import ConversationalRetrievalChain
from htmltemplates import css, bot_template, user_template
import langcheck


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
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

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
            
    return st.session_state.chat_history


def main():
    load_dotenv()
    st.set_page_config(page_title="GPT Summariser", page_icon=":whale:")
    st.write(css, unsafe_allow_html=True)

    # Initialise as empty string and update whenever files are processed
    source_text = "" 

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("LangChain-enabled GPT Summariser :whale:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        # Retrieving AI answer
        queries_answers = handle_user_input(user_question)
        ai_answer = queries_answers[-1].content

        # Adding fluency score into main 
        fluency_score = langcheck.metrics.fluency(ai_answer).metric_values[0]

        # Adding factual consistency score
        factual_consistency_score = langcheck.metrics.en.source_based_text_quality.factual_consistency(generated_outputs= ai_answer,
                                                                                                       sources = source_text,
                                                                                                       prompts= user_question,
                                                                                                       model_type= 'local').metric_values[0]
        print(f'This answer has a fluency score of: {fluency_score}')
        print(f'This answer has an accuracy score of: {factual_consistency_score}')
            

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Process'", accept_multiple_files=False)
        if st.button("Process"):
            with st.spinner("Processing"):
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