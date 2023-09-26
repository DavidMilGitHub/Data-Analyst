import os
import streamlit as st
from transformers import GPT2TokenizerFast
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
import fitz  # PyMuPDF

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "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"

# Create a Streamlit app
st.title("Dental Practice")

# URL of the PDF file on GitHub (replace with your actual GitHub URL)
pdf_github_url = "https://github.com/DavidMilGitHub/Data-Analyst/blob/main/test_folder/docs/DentalClinicManual.pdf"

# Initialize pdf_content as an empty string
pdf_content = ""

# Fetch the PDF content from GitHub
try:
    response = requests.get(pdf_github_url)
    if response.status_code == 200:
        pdf_content = response.content.decode('utf-8')
    else:
        st.warning("Failed to fetch the PDF. Please check the URL.")
except Exception as e:
    st.warning("An error occurred while fetching the PDF: " + str(e))

# Create function to count tokens
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=24,
    length_function=count_tokens,
)

chunks = text_splitter.create_documents([pdf_content])

# Get embedding model
embeddings = OpenAIEmbeddings()

# Create vector database
db = FAISS.from_documents(chunks, embeddings)

# Create QA chain
chain = load_qa_chain(OpenAI(temperature=0.5), chain_type="stuff")

# User input query
query = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if query:
        # Perform similarity search to get documents
        docs = db.similarity_search(query)

        # Run the QA chain with input documents and question
        result = chain.run(input_documents=docs, question=query)

        # Display the answer
        st.write("Answer:", result)
    else:
        st.warning("Please enter a question.")
