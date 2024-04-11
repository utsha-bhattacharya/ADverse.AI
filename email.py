import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from conversational import get_conversational_chain

# Function to generate email content
def generate_email(user_question=None, recipient_name=None, recipient_email=None, email_content=None, tone=None):
    if user_question:
        # Generate email content using conversational AI
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
        docs = new_db.similarity_search(user_question)
        chain = get_conversational_chain("gemini-pro")
        response = chain(
            {"input_documents": docs, "platform": "Email", "context": "Email content", "question": user_question},
            return_only_outputs=True
        )
        st.write("Email Content: ", response["output_text"])
    elif recipient_name and recipient_email and email_content and tone:
        # Generate email content based on user inputs
        if tone == "Formal":
            email_greeting = f"Dear {recipient_name},\n\n"
        else:
            email_greeting = f"Hi {recipient_name},\n\n"
            
        email = f"{email_greeting}{email_content}\n\nBest regards,\nYour Name"
        st.write("Generated Email:", email)
    else:
        st.error("Please provide either a user question or recipient information along with email content and tone.")
