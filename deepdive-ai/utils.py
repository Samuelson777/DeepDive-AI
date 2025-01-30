import PyPDF2
import google.generativeai as genai
from dotenv import load_dotenv
import os

def extract_text(uploaded_file):
    """Extract text from PDF files."""
    if uploaded_file.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    return ""

def generate_response(full_text, query, api_key):
    """Generate a response based on the query and extracted text using Google Generative AI."""
    # Configure the Google Generative AI API with the user's API key
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    # Start a chat session with context about the uploaded PDF
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": "I have uploaded a paper. Please only answer questions based on the content of the paper provided below:\n\n" + full_text},
            {"role": "model", "parts": "Understood. I will only provide information based on the content of the uploaded paper."}
        ]
    )
    
    # Send the user's query
    response = chat.send_message(query, stream=True)
    
    # Collect and return the response
    response_text = ""
    for chunk in response:
        response_text += chunk.text
    
    return response_text