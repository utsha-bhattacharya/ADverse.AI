import streamlit as st
from conversational import get_pdf_text, get_text_chunks,get_vector_store
from linkedin import generate_linkedin_post
from twitter import  generate_twitter_post
from facebook import generate_facebook_post


def generate_document_content(user_question, platform, pdf_docs):
    if pdf_docs:
        raw_text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        st.success("Data has been successfully stored.")

    if user_question:
        if platform == "LinkedIn":
            generate_linkedin_post(user_question)
        elif platform == "Twitter":
            generate_twitter_post(user_question)
        elif platform == "Facebook":
            generate_facebook_post(user_question)
