import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from conversational import get_conversational_chain

# Function to generate Twitter post
def generate_twitter_post(user_question, tone):
    context = "Write a Twitter post highlighting important points in 1-2 Lines"
    # Adjust context based on tone
    if tone == 'Negative':
        context = "Write a Twitter post highlighting important points in 1-2 Lines - Addressing Concerns"
    elif tone == 'Positive':
        context = "Write a Twitter post highlighting important points in 1-2 Lines - Highlighting Strengths"
    elif tone == 'Formal':
        context = "Write a formal Twitter post highlighting key points in 1-2 Lines"
    elif tone == 'Academic':
        context = "Compose an academic-style Twitter post, covering significant aspects in 1-2 Lines"
    elif tone == 'Creative':
        context = "Craft a creative Twitter post, exploring important points through imaginative language in 1-2 Lines"
    elif tone == 'Simple':
        context = "Draft a straightforward Twitter post, summarizing key aspects in 1-2 Lines"
    elif tone == 'Critical Analysis':
        context = "Provide a critical analysis in a Facebook post, examining important points in 1-2 Lines"
    elif tone == 'Standard' or tone == 'Fluent':
        context = "Write a Twitter post highlighting important points 1-2 Lines"

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain("gemini-pro")
    response = chain(
        {"input_documents": docs, "platform": "Twitter", "context": "Single line post about company's expertise", "question": user_question},
        return_only_outputs=True
    )
   
    st.write("Reply: ", response["output_text"])
