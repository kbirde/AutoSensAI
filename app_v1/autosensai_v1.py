import streamlit as st
import os
import openai
import PyPDF2
import requests
from io import BytesIO

# Initialize OpenAI API key (replace with your actual key)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Secure API key from Streamlit Cloud Secrets

def get_response_from_llm(question, passage):
    # Combine the question and passage to create a prompt for the LLM
    prompt = f"Answer the following question based on the provided passage:\n\nPassage:\n{passage}\n\nQuestion: {question}\nAnswer:"

    # Use the new ChatCompletion API (note the change from openai.Completion.create to openai.ChatCompletion.create)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,  # Adjust as needed
        temperature=0.7,
    )

    # Extract the response content
    return response['choices'][0]['message']['content'].strip()

def extract_text_from_pdf(pdf_url):
    # Fetch the PDF from the provided URL (e.g., GitHub raw URL)
    response = requests.get(pdf_url)
    if response.status_code == 200:
        pdf_data = response.content
        reader = PyPDF2.PdfReader(BytesIO(pdf_data))
        full_text = ""
        # Extract text from all pages of the PDF
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            if text:
                full_text += text
        return full_text
    else:
        return "Error: Could not fetch the PDF from the URL"

# Streamlit app
st.markdown("<h1 style='text-align: center;'>AutoSensAI</h1>", unsafe_allow_html=True)

# Set the path to the 'manuals' directory
manuals_directory = os.path.join(os.path.dirname(__file__), 'manuals')

# Initialize session state for conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

# Get list of manual options
manual_options = ["Select a Car Manual"] + [f for f in os.listdir(manuals_directory) if f.endswith('.pdf')]

# Dropdown for selecting car manual without a header
selected_manual = st.selectbox("", manual_options)

# Store the selected manual in session state
st.session_state.selected_manual = selected_manual

# Fetch and display text from the selected manual (only if a manual is selected)
if selected_manual != "Select a Car Manual":
    github_raw_url = f"https://raw.githubusercontent.com/yourusername/AutoSensAI/main/manuals/{selected_manual}"
    manual_text = extract_text_from_pdf(github_raw_url)

    # Display a preview of the extracted text
    st.write("Extracted Text from Manual (partial):")
    st.write(manual_text[:1000])  # Show first 1000 characters for preview

# User input for the question
user_input = st.text_input("You: ", "")

if user_input and selected_manual != "Select a Car Manual":
    # Find the most relevant passage based on the user's input (simple approach for now)
    relevant_passage = manual_text[:1000]  # Extract the first 1000 characters (you can refine this)

    # Get the response from the LLM based on the user's question and the relevant passage
    response = get_response_from_llm(user_input, relevant_passage)
    
    # Append the conversation history
    st.session_state.history.append(f"You: {user_input}")
    st.session_state.history.append(f"Chatbot: {response}")

# Display the conversation history
for message in st.session_state.history:
    st.text(message)
