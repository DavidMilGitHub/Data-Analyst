
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
import requests



def get_pdf_text(pdf_file_path):
    text = ""
    pdf_reader = PdfReader(pdf_file_path)
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
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
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

def handle_userinput(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

import requests
import pdfplumber
import io


github_txt_url = 'https://raw.githubusercontent.com/DavidMilGitHub/Data-Analyst/main/DentalBot/dental.txt'


def fetch_txt_from_github(txt_url):
    try:
        response = requests.get(txt_url)
        response.raise_for_status()  # Check if the request was successful
        return response.text
    except Exception as e:
        st.error("An error occurred while fetching the text file: " + str(e))
        return None




# Define other functions (get_text_chunks, get_vectorstore, get_conversation_chain, handle_userinput) as before

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with PDF", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with PDF :books:")

    # Specify the GitHub raw content URL of the PDF file
    github_pdf_url = "https://github.com/DavidMilGitHub/Data-Analyst/blob/7ee33a509e4c73903152a0505cd93540d35119aa/DentalBot/DentalClinicManual.pdf"

    # Get PDF text from the GitHub URL
    # raw_text = get_pdf_text(github_pdf_url)
    raw_text = fetch_txt_from_github(github_txt_url)

    # Get PDF text
        # raw_text = get_pdf_text(pdf_file_path)

    # Get the text chunks
    text_chunks = get_text_chunks(raw_text)

    # Create vector store
    vectorstore = get_vectorstore(text_chunks)

    # Create conversation chain
    st.session_state.conversation = get_conversation_chain(vectorstore)
    
    user_question = st.text_input("Ask a question about the PDF:")
    if user_question:
        handle_userinput(user_question)

if __name__ == '__main__':
    main()

