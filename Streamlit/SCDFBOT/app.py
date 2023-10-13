import streamlit as st
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import os
import openai
import requests

# Set your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

# Initialize your chatbot components (document, loader, embeddings, etc.)
# ... (Code you provided in your question)
document=[]
# pdf_path="C:\\Users\\user\\Desktop\\CLAUSE3.pdf"
# loader=PyPDFLoader(pdf_path)
# document.extend(loader.load())
# Specify the URL of the PDF file on GitHub


github_pdf_url = "https://github.com/DavidMilGitHub/Data-Analyst/blob/7ee33a509e4c73903152a0505cd93540d35119aa/DentalBot/DentalClinicManual.pdf"
response = requests.get(github_pdf_url)
raw_text = response.txt

document.extend(raw_text)

document_splitter=CharacterTextSplitter(separator='\n', chunk_size=500, chunk_overlap=100)

document_chunks=document_splitter.split_documents(document)

embeddings = OpenAIEmbeddings()

vectordb=Chroma.from_documents(document_chunks,embedding=embeddings)#, persist_directory='./data')

# vectordb.persist()

llm=ChatOpenAI(temperature=0.3, model_name='gpt-3.5-turbo',max_tokens=256)


memory=ConversationBufferMemory(memory_key='chat_history', return_messages=True)

#Create our Q/A Chain
pdf_qa=ConversationalRetrievalChain.from_llm(llm=llm,
                                             retriever=vectordb.as_retriever(search_kwargs={'k':6}),
                                             verbose=False, memory=memory)



# Define a function to get the chatbot response
def get_chatbot_response(question):
    result = pdf_qa({"question": question})
    return result['answer'], result.get('source', '')



def main():
    # Create a Streamlit app
    st.title("Chatbot App")
    
    # Add a text input field for user questions
    user_question = st.text_input("Ask a question")

    # Check if the user has entered a question
    if user_question:
        # Get the chatbot's response
        chatbot_response, source = get_chatbot_response(user_question)
        st.write("Chatbot Response:")
        st.write(chatbot_response)

        if source:
            st.write("Source:")
            st.write(source)
# Run the Streamlit app
if __name__ == "__main__":
    main()
