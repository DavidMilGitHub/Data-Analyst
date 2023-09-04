import streamlit as st
from difflib import SequenceMatcher
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download NLTK data (only required once)
nltk.download("punkt")
nltk.download("wordnet")

# Initialize the WordNet Lemmatizer
lemmatizer = WordNetLemmatizer()

# Load your JSON data
try:
    with open('github.com/DavidMilGitHub/Data-Analyst/blob/main/Streamlit/your_dataset.json', 'r') as json_file:
        qa_data = json.load(json_file)
except FileNotFoundError:
    st.error("Dataset file not found. Please make sure 'your_dataset.json' exists.")

st.title('Question Answering Chatbot')

# User's question input
user_question = st.text_input('Enter your question:')

if st.button('Get Answer'):
    if not user_question:
        st.warning("Please enter a question.")
    else:
        # Function to calculate Jaccard similarity
        def calculate_jaccard_similarity(set1, set2):
            intersection = len(set1.intersection(set2))
            union = len(set1.union(set2))
            return intersection / union if union != 0 else 0

        # Lemmatize and tokenize the user's question
        user_question_tokens = [lemmatizer.lemmatize(token.lower()) for token in word_tokenize(user_question)]

        # Function to preprocess and tokenize text
        def preprocess_and_tokenize(text):
            return [lemmatizer.lemmatize(token.lower()) for token in word_tokenize(text)]

        # Function to find the most similar question in the dataset
        @st.cache_data
        def find_most_similar_question(user_question, data):
            max_similarity = 0
            most_similar_question = None

            for entry in data:
                question_tokens = preprocess_and_tokenize(entry["question"])
                text_similarity = SequenceMatcher(None, user_question_tokens, question_tokens).ratio()

                if text_similarity > max_similarity:
                    max_similarity = text_similarity
                    most_similar_question = entry

            return most_similar_question

        # Find the most similar question in the dataset
        similar_question = find_most_similar_question(user_question, qa_data)

        # Retrieve the answer based on the similar question
        if similar_question:
            answer = similar_question["answer"]
            st.subheader('Answer:')
            st.write(answer)
        else:
            st.info('No matching question found.')


# import streamlit as st
# import json
# import spacy
# from spacy.tokens import Doc
# from difflib import SequenceMatcher

# # Load your JSON data
# try:
#     with open('your_dataset.json', 'r') as json_file:
#         qa_data = json.load(json_file)
# except FileNotFoundError:
#     st.error("Dataset file not found. Please make sure 'your_dataset.json' exists.")

# st.title('Question Answering Chatbot')

# # Load the spaCy language model
# nlp = spacy.load("en_core_web_sm")

# # User's question input
# user_question = st.text_input('Enter your question:')

# if st.button('Get Answer'):
#     if not user_question:
#         st.warning("Please enter a question.")
#     else:
#         # Function to calculate Jaccard similarity
#         def calculate_jaccard_similarity(set1, set2):
#             intersection = len(set1.intersection(set2))
#             union = len(set1.union(set2))
#             return intersection / union if union != 0 else 0

#         # Preprocess and tokenize the user's question with spaCy
#         user_question_doc = nlp(user_question.lower())

#         # Function to preprocess and tokenize text with spaCy
#         def preprocess_and_tokenize(text):
#             return nlp(text.lower())

#         # Function to find the most similar question in the dataset
#         @st.cache_data
#         def find_most_similar_question(user_question, data):
#             max_similarity = 0
#             most_similar_question = None

#             for entry in data:
#                 question_doc = preprocess_and_tokenize(entry["question"])
#                 text_similarity = SequenceMatcher(None, user_question_doc.text, question_doc.text).ratio()

#                 if text_similarity > max_similarity:
#                     max_similarity = text_similarity
#                     most_similar_question = entry

#             return most_similar_question

#         # Find the most similar question in the dataset
#         similar_question = find_most_similar_question(user_question, qa_data)

#         # Retrieve the answer based on the similar question
#         if similar_question:
#             answer = similar_question["answer"]
#             st.subheader('Answer:')
#             st.write(answer)
#         else:
#             st.info('No matching question found.')
