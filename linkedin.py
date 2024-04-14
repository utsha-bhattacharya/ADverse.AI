import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from conversational import get_conversational_chain

# Function to generate LinkedIn post
def generate_linkedin_post(user_question, tone):
    context = "Write a LinkedIn post highlighting important points in 2-3 paragraphs"
    if tone == 'Negative':
        context = "Write a LinkedIn post highlighting important points in 2-3 paragraphs - Addressing Concerns"
    elif tone == 'Positive':
        context = "Write a LinkedIn post highlighting important points in 2-3 paragraphs - Highlighting Strengths"
    elif tone == 'Formal':
        context = "Write a formal LinkedIn post highlighting key points in 2-3 paragraphs"
    elif tone == 'Academic':
        context = "Compose an academic-style LinkedIn post, covering significant aspects in 2-3 paragraphs"
    elif tone == 'Creative':
        context = "Craft a creative LinkedIn post, exploring important points through imaginative language in 2-3 paragraphs"
    elif tone == 'Simple':
        context = "Draft a straightforward LinkedIn post, summarizing key aspects in in 2-3 paragraphs"
    elif tone == 'Critical Analysis':
        context = "Provide a critical analysis in a LinkedIn post, examining important points in 2-3 paragraphs"
    elif tone == 'Standard' or tone == 'Fluent':
        context = "Write a Facebook post highlighting important points in 2-3 paragraphs"
        
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain("gemini-pro")
    response = chain(
        {"input_documents": docs, "platform": "LinkedIn", "context": context, "question": user_question},
        return_only_outputs=True
    )
    
    st.write("Reply: ", response["output_text"])


