import requests
from bs4 import BeautifulSoup
import streamlit as st
def scrape_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract relevant text or information from the website
        # Here, we're extracting all text from paragraphs and headers
        text = ''
        for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text += tag.get_text() + ' '
        return text
    else:
        st.error(f"Failed to scrape the website {url}. Please check the URL.")