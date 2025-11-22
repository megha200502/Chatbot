import os
import json
import streamlit as st
import google.generativeai as genai
import PyPDF2

#Page Config
st.set_page_config(page_icon="🗪", page_title="gpt.4o chat")

# Setup
working_dir = os.path.dirname(os.path.abspath(__file__))
config_path = f"{working_dir}/config.json"

if not os.path.exists(config_path):
    st.error("Config file not found!")
    st.stop()

config_data = json.load(open(config_path))
genai.configure(api_key=config_data["GOOGLE_API_KEY"])

# Session State Init
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if 'pdf_context' not in st.session_state:
    st.session_state.pdf_context = "You are a helpful assistant." # Default instruction
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

# Helper Functions
def get_pdf_text(file_path):
    text = ""
    try:
        pdf_reader = PyPDF2.PdfReader(file_path)
        for page in pdf_reader.pages:
            text += page.extract_text()
    except:
        pass
    return text

def toggle_clicked():
    st.session_state.clicked = not st.session_state.clicked

st.title("🤖 GPT-4o -CHATBOT")

col1, col2 = st.columns([4, 1])
with col2:
    if st.session_state.clicked:
        st.button("Close Upload", on_click=toggle_clicked)
    else:
        st.button("Upload PDF", on_click=toggle_clicked)

if st.session_state.clicked:
    uploaded_files = st.file_uploader("Upload PDF", type=["pdf"], accept_multiple_files=True)
    if uploaded_files:
        if not os.path.exists("data"): os.makedirs("data")
        
        full_text = ""
        for uploaded_file in uploaded_files:
            file_path = f"data/{uploaded_file.name}"
            with open(file_path, "wb") as f: f.write(uploaded_file.getbuffer())
            full_text += get_pdf_text(file_path) + "\n"
        
       
        st.session_state.pdf_context = f"Here is the knowledge base you must use to answer: \n{full_text}"
        st.success("Memory Updated via System Instruction!")

# Chat History Display
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# MAIN LOGIC 
user_prompt = st.chat_input("Ask me anything...")

if user_prompt:
    # User message show karo
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    
    gemini_history = []
    for msg in st.session_state.chat_history[:-1]: # Last wala abhi nahi jodenge, wo send_message me jayega
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})

    # Model Initialize 
    
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        system_instruction=st.session_state.pdf_context
    )

    # Chat Session Start 
    chat = model.start_chat(history=gemini_history)

    #  Response Generate
    try:
        with st.spinner("Thinking..."):
            response = chat.send_message(user_prompt)
            assistant_response = response.text

        with st.chat_message("assistant"):
            st.markdown(assistant_response)
        
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    except Exception as e:
        st.error(f"Error: {e}")