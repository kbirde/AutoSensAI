import streamlit as st
import os
import openai
import PyPDF2

# Initialize OpenAI API key (replace with your actual key)
openai.api_key = 'your-openai-api-key'

def get_response_from_llm(question, passage):
    # Combine the question and passage to create a prompt
    prompt = f"Answer the following question based on the provided passage:\n\nPassage:\n{passage}\n\nQuestion: {question}\nAnswer:"

    # Send the prompt to the OpenAI API and get the response
    response = openai.Completion.create(
        model="gpt-3.5-turbo",  # You can change this to another model (like gpt-4)
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,  # Adjust as necessary
        temperature=0.7,
    )

    # Extract the text of the response
    return response['choices'][0]['message']['content'].strip()

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        full_text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            full_text += page.extract_text()
    return full_text

# Streamlit app
st.markdown("<h1 style='text-align: center;'>AutoSensAI</h1>", unsafe_allow_html=True)

manuals_directory = os.path.join(os.path.dirname(__file__), 'manuals')

# Initialize session state for conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

# Set the options for the dropdown, including the default message
manual_options = ["Select a Car Manual"] + [f for f in os.listdir(manuals_directory) if f.endswith('.pdf')]

# Dropdown for selecting car manual without a header
selected_manual = st.selectbox("", manual_options)

# Store the selected manual in session state
st.session_state.selected_manual = selected_manual

# Extract and display text from the selected manual
if selected_manual != "Select a Car Manual":
    pdf_path = os.path.join(manuals_directory, selected_manual)
    manual_text = extract_text_from_pdf(pdf_path)
    st.write("Extracted Text from Manual (partial):")
    st.write(manual_text[:1000])  # Display a preview of the extracted text

# User input for question
user_input = st.text_input("You: ", "")

if user_input and selected_manual != "Select a Car Manual":
    # Extract the relevant passage from the manual based on the user query (simple approach)
    # You might want to implement more sophisticated search algorithms (like TF-IDF or embedding search) here
    relevant_passage = manual_text[:1000]  # For simplicity, we're just using the first 1000 characters
    response = get_response_from_llm(user_input, relevant_passage)
    
    # Append the conversation to the history
    st.session_state.history.append(f"You: {user_input}")
    st.session_state.history.append(f"Chatbot: {response}")

# Display conversation history
for message in st.session_state.history:
    st.text(message)
