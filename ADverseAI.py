import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from bs4 import BeautifulSoup
import requests
from openai import OpenAI

# Function to extract text from PDF documents
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to split text into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create and save vector store
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

# Function to load conversational chain
def get_conversational_chain(model_name):
    prompt_template = """
    Generate a social media post for {platform}:\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model=model_name, temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["platform", "context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain
#________________________________________________________________________________________
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

#________________________________________________________________________________________

# Function to generate Twitter post
def generate_twitter_post(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain("gemini-pro")
    response = chain(
        {"input_documents": docs, "platform": "Twitter", "context": "Single line post about company's expertise", "question": user_question},
        return_only_outputs=True
    )
   
    st.write("Reply: ", response["output_text"])

#________________________________________________________________________________________

# Function to scrape website and generate content
def generate_website_content(user_question, platform, website_urls):
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
            generate_linkedin_post(user_question)
        elif platform == "Twitter":
            generate_twitter_post(user_question)

#________________________________________________________________________________________

#Function to generate AI based images 
def generate_images_using_openai(text, num_images=3, resolution=(256, 256)):
    # Map resolution to width and height
    resolution_mapping = {
        (256, 256): (256, 256),
        (512, 512): (512, 512),
        (1024, 1024): (1024, 1024)
    }

    # Ensure resolution is one of the available options, default to 256x256 otherwise
    width, height = resolution_mapping.get(resolution, (256, 256))

    client = OpenAI()
    response = client.images.generate(prompt=text, n=num_images, size=f"{width}x{height}")
    image_urls = [image_data.url for image_data in response.data]
    return image_urls

#________________________________________________________________________________________
   
# Function to scrape website
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

#________________________________________________________________________________________

# Function to store data in vector database

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

#________________________________________________________________________________________

def main():
    st.set_page_config(page_title="ADverse.AI" , layout="wide")

    st.markdown(
        """
        <style>
        .sidebar .sidebar-content {
            background-color: #453bd4;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    logo = open('C:\\Users\\suddh\\OneDrive\\Documents\\LangChain\\ADverse.Ai\\logo.png','rb').read()

    # Display the image and text in the sidebar
    st.sidebar.image(logo, width=100)
    st.sidebar.markdown("""
        <div style='display: inline-block; vertical-align: top;'>
            <h1 style='margin-bottom: 0px;'>ADverse.AI</h1>
            <p style='margin-top: 0px;'>Description</p>
            <p>This tool helps you generate social media posts for LinkedIn, Twitter and generate image based on either documents uploaded by the user or text scraped from websites.</p>
            <hr>
        </div>
        """,
        unsafe_allow_html=True)

    user_choice = st.sidebar.radio("Navigation", ["Document Content Generation", "Website Content Generation", "Image Generation"])

    if user_choice == "Document Content Generation":
        st.subheader("Get Social-Media Content for your Document")
        st.sidebar.markdown("### Document Content Generation")
        pdf_docs = st.file_uploader("Upload your PDF Files", accept_multiple_files=True)
        user_question = st.text_input("Enter your question or prompt:")
        platform = st.sidebar.selectbox("Select platform", ["LinkedIn", "Twitter"])
        if st.button("Generate Post"):
            with st.spinner("Generating..."):
                generate_document_content(user_question, platform, pdf_docs)

    elif user_choice == "Website Content Generation":
        st.subheader("Get Social-Media Content for your Website")
        st.sidebar.markdown("### Website Content Generation")
        website_urls = st.text_area("Enter the URLs of websites(one URL per line)", '',height = 50)
        user_question = st.text_input("Enter your question or prompt:")
        platform = st.sidebar.selectbox("Select platform", ["LinkedIn", "Twitter"])
        if st.button("Generate Content"):
            with st.spinner("Generating..."):
                generate_website_content(user_question, platform, website_urls.split("\n"))

    elif user_choice == "Image Generation":
        st.subheader("Generate AI-Based Images")
        #st.sidebar.markdown("### Image Generation")
        user_prompt = st.text_input("Enter your prompt or text for generating image:")
        num_images = st.number_input("Number of images to generate", min_value=1, max_value=10, value=3)
        resolution_options = {
            "256x256": (256, 256),
            "512x512": (512, 512),
            "1024x1024": (1024, 1024)
        }
        selected_resolution = st.selectbox("Resolution", list(resolution_options.keys()), index=0)
        resolution = resolution_options[selected_resolution]

        if st.button("Generate Image"):
            with st.spinner("Generating..."):
                image_urls = generate_images_using_openai(user_prompt, num_images, resolution)
                for idx, image_url in enumerate(image_urls):
                    st.image(image_url, caption=f"Generated Image {idx+1}", use_column_width=True)


if __name__ == "__main__":
    main()
