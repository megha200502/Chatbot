import streamlit as st
import requests

st.set_page_config(page_title="AI Chat UI")

st.title("💬 AI Chatbot")
st.write("This UI sends your message to the FastAPI backend and displays the response.")

API_URL = "http://127.0.0.1:8000/generate"

user_input = st.text_input("Enter your prompt:")

if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please write something first.")
    else:
        with st.spinner("Generating response..."):
            try:
                response = requests.post(API_URL, json={"prompt": user_input})

                if response.status_code == 200:
                    st.success(response.json().get("response"))
                else:
                    st.error("API Error: " + response.text)

            except Exception as e:
                st.error("Connection Error: " + str(e))
