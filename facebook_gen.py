from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from conversational import get_conversational_chain
import streamlit as st 

# Function to create Facebook post
def generate_facebook_post(user_question, tone):
    context = "Write a Facebook post highlighting important points in 3-6 paragraphs"
    # Adjust context based on tone
    if tone == 'Negative':
        context = "Write a Facebook post highlighting important points in 3-6 paragraphs - Addressing Concerns"
    elif tone == 'Positive':
        context = "Write a Facebook post highlighting important points in 3-6 paragraphs - Highlighting Strengths"
    elif tone == 'Formal':
        context = "Write a formal Facebook post highlighting key points in 3-6 paragraphs"
    elif tone == 'Academic':
        context = "Compose an academic-style Facebook post, covering significant aspects in 3-6 paragraphs"
    elif tone == 'Creative':
        context = "Craft a creative Facebook post, exploring important points through imaginative language in 3-6 paragraphs"
    elif tone == 'Simple':
        context = "Draft a straightforward Facebook post, summarizing key aspects in 3-6 paragraphs"
    elif tone == 'Critical Analysis':
        context = "Provide a critical analysis in a Facebook post, examining important points in 3-6 paragraphs"
    elif tone == 'Standard' or tone == 'Fluent':
        context = "Write a Facebook post highlighting important points in 3-6 paragraphs"

    # Initialize embeddings and vector store
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    
    # Performing similarity search
    docs = new_db.similarity_search(user_question)
    
    # Getting conversational chain
    chain = get_conversational_chain("gemini-pro")
    
    # Generating response
    response = chain(
        {"input_documents": docs, "platform": "Facebook", "context": context, "question": user_question},
        return_only_outputs=True
    )
   
    st.write("Reply: ", response["output_text"])
