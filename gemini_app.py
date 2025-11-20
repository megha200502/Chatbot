import os
import json
import streamlit as st
import google.generativeai as genai

working_dir = os.path.dirname(os.path.abspath(__file__))
config_data = json.load(open(f"{working_dir}/config.json"))
google_api_key = config_data["GOOGLE_API_KEY"]

# Configure Gemini
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel("gemini-2.5-flash")

# Streamlit settings
st.set_page_config(
    page_title="gpt.4o chat",
    page_icon="🗪",
    layout="centered"
)

# Chat session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Title
st.title("🤖 GPT-4o -CHATBOT")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_prompt = st.chat_input("ASK GPT.4O....")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

# -------------------------------
# FIXED: Gemini response section
# -------------------------------
if user_prompt:
    # Convert your chat history to Gemini's expected format
    gemini_messages = [
        {"role": "user", "parts": m["content"]}
        if m["role"] == "user"
        else {"role": "model", "parts": m["content"]}
        for m in st.session_state.chat_history
    ]

    # Generate response
    response = model.generate_content(gemini_messages)
    assistant_response = response.text

    # Save in session
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": assistant_response
    })

    # Display assistant reply
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
