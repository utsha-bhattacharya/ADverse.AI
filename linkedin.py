import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from conversational import get_conversational_chain
import os

from authtoken import GOOGLE_API_KEY,OPENAI_API_KEY
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
# Function to generate LinkedIn post
def generate_linkedin_post(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain("gemini-pro")
    response = chain(
        {"input_documents": docs, "platform": "LinkedIn", "context": "Company's expertise and field of work", "question": user_question},
        return_only_outputs=True
    )
    
    st.write("Reply: ", response["output_text"])
