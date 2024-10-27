import streamlit as st
import os

def get_response(user_input):
    responses = {
        "hello": "Hi there! How can I help you?",
        "how are you?": "I'm just a bunch of code, but thanks for asking!",
        "bye": "Goodbye! Have a great day!",
    }
    return responses.get(user_input.lower(), "I don't understand that.")

# Streamlit app
st.markdown("<h1 style='text-align: center;'>AutoSensAI</h1>", unsafe_allow_html=True)

# Check the current working directory
st.write("Current working directory:", os.getcwd())
st.write("Contents of the current directory:", os.listdir('.'))

#manuals_directory = "manuals"
manuals_directory = os.path.join(os.path.dirname(__file__), 'manuals')
st.write("Manuals directory exists:", os.path.exists(manuals_directory))

if os.path.exists(manuals_directory):
    manual_files = [f for f in os.listdir(manuals_directory) if f.endswith('.pdf')]
    st.write("Manual files found:", manual_files)
else:
    st.write("No manual files found.")
    
## Load PDF manuals from the 'manuals' directory
#manuals_directory = 'manuals'
#print("Manuals directory exists:", os.path.exists(manuals_directory))
#manual_files = [f for f in os.listdir(manuals_directory) if f.endswith('.pdf')]

# Initialize session state for conversation history
if 'history' not in st.session_state:
    st.session_state.history = []

# Set the options for the dropdown, including the default message
manual_options = ["Select a Car Manual"] + manual_files  # Add the default message

# Dropdown for selecting car manual without a header
selected_manual = st.selectbox("", manual_options)

# Store the selected manual in session state
st.session_state.selected_manual = selected_manual

# User input
user_input = st.text_input("You: ", "")

if user_input:
    response = get_response(user_input)
    st.session_state.history.append(f"You: {user_input}")
    st.session_state.history.append(f"Chatbot: {response}")

# Display conversation history
for message in st.session_state.history:
    st.text(message)
