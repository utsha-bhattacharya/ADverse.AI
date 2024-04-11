import streamlit as st

#________________________________________________________________________________
#external functions 
from docgen import generate_document_content
from website import generate_website_content
from image import generate_images_using_openai
from email import generate_email


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

    logo = open('logo.png','rb').read()

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

    user_choice = st.sidebar.radio("Navigation", ["Document Content Generation", "Website Content Generation", "Image Generation", "Email Generation"])

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
     elif user_choice == "Email Generation":
        user_question = st.text_input("Enter your question or prompt:")
        recipient_name = st.text_input("Recipient Name")
        recipient_email = st.text_input("Recipient Email")
        email_content = st.text_area("Email Content")
        tone = st.selectbox("Tone", ["Formal", "Informal"])

        if st.button("Generate Email"):
            generate_email(user_question=user_question)

        if st.button("Generate Custom Email"):
            generate_email(recipient_name=recipient_name, recipient_email=recipient_email, email_content=email_content, tone=tone)




if __name__ == "__main__":
    main()
