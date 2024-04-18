import streamlit as st
from scrape import scrape_website
from conversational import get_vector_store, get_text_chunks
from linkedin import generate_linkedin_post
from twitter import  generate_twitter_post
from facebook_gen import generate_facebook_post

# Function to scrape website and generate content
def generate_website_content(user_question, platform, website_urls, tone):
    # Scraping data from websites
    scraped_texts = []
    for url in website_urls:
        if url:
            scraped_text = scrape_website(url)
            if scraped_text:
                scraped_texts.append(scraped_text)

    # Storing data in vector database
    if scraped_texts:
        text_chunks = [chunk for text in scraped_texts for chunk in get_text_chunks(text)]
        get_vector_store(text_chunks)
        st.success("Data has been successfully stored.")

    if user_question:
        if platform == "LinkedIn":
            generate_linkedin_post(user_question, tone)
        elif platform == "Twitter":
            generate_twitter_post(user_question, tone)
        elif platform == "Facebook":
            generate_facebook_post(user_question, tone)
