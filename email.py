from conversational import get_email_chain
import streamlit as st
from langchain_google_genai import GoogleGenerativeAIEmbeddings

def generate_automated_email(recipient_name, recipient_email, email_context):

    # Generate email template using Gemini model
    chain =  get_email_chain("gemini-pro")
    response = chain(
        {"recipient_name": recipient_name, "recipient_email": recipient_email, "email_context": email_context},
        return_only_outputs=True
    )
    # Display the generated email template
    st.subheader("Generated Email Template:")
    st.write("Reply: ", response["text"])
