from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain

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

# Function to load email
def get_email_chain(model_name):
    prompt_template = """
    Generate an email for {recipient_name} ({recipient_email}):\n\n{email_context}
    Answer:
    """

    model = ChatGoogleGenerativeAI(model=model_name, temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["recipient_name", "recipient_email", "email_context"])
    chain = LLMChain(prompt=prompt, llm = model)
    return chain
