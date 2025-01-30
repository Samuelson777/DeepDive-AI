import streamlit as st
from utils import extract_text, generate_response

# Set the page configuration as the first command
st.set_page_config(page_title="DeepDive AI - PaperInsight", layout="wide")

# Load custom CSS
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Title of the app
st.title("DeepDive AI - PaperInsight")
st.markdown("### Get insights from your AI research papers!")

# Sidebar for user inputs
st.sidebar.header("User   Input")
api_key = st.sidebar.text_input("Enter your Google Generative AI API Key:", type="password")
uploaded_file = st.sidebar.file_uploader("Upload your AI research paper (PDF format)", type="pdf")

# Main content area
st.markdown("### Ask Questions About Your Paper")
if uploaded_file is not None:
    # Extract text from the uploaded PDF
    full_text = extract_text(uploaded_file)
    st.success("Text extracted successfully! You can now ask questions about the paper.")

    # User Query Input
    user_query = st.text_input("Ask a question about the paper:")

    if st.button("Get Answer"):
        if api_key:
            with st.spinner("Generating response..."):
                # Generate response using the user's API key
                response = generate_response(full_text, user_query, api_key)
                
                # Display the user query and the response clearly
                st.markdown("### Your Question:")
                st.write(user_query)
                
                st.markdown("### Chatbot Response:")
                
                # Check for dark mode or light mode
                if st.session_state.get('dark_mode', False):
                    st.markdown(f'<div class="chatbot-response-dark">{response}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chatbot-response">{response}</div>', unsafe_allow_html=True)
        else:
            st.error("Please enter a valid API key.")
else:
    st.info("Please upload a PDF file to get started.")