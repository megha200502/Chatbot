import streamlit as st
import requests

st.set_page_config(page_title="AI Streaming Chat")

st.title("💬 Streaming AI Chatbot")

API_URL = "http://127.0.0.1:8000/stream"

user_input = st.text_input("Enter your message:")

if st.button("Send"):
    if not user_input.strip():
        st.warning("Please enter something.")
    else:
        with st.spinner("Streaming..."):
            try:
                response = requests.post(API_URL, json={"prompt": user_input}, stream=True)

                output = st.empty()
                final_text = ""

                for chunk in response.iter_content(chunk_size=None):
                    text = chunk.decode("utf-8")
                    final_text += text
                    output.markdown(final_text)

            except Exception as e:
                st.error(f"Error: {e}")
