import streamlit as st
import json
import os
import requests

API_URL = "http://127.0.0.1:8000/pdf_chat"
USER_FILE = "users.json"

# Create users file
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Session variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = ""

if "history" not in st.session_state:
    st.session_state.history = []


# -------------------------- CHATBOT PAGE --------------------------
if st.session_state.logged_in:

    # -------- SIDEBAR HISTORY --------
    with st.sidebar:
        st.title("📜 Chat History")

        # Show chat questions in sidebar
        for i, item in enumerate(st.session_state.history):
            if st.button(item["q"], key=f"history_{i}"):
                st.write("### **Selected Chat**")
                st.write(f"**Q:** {item['q']}")
                st.write(f"**A:** {item['a']}")

        # Clear history button
        if st.button("🗑 Clear History"):
            st.session_state.history = []
            st.rerun()

        # Logout button
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = ""
            st.rerun()


    # -------- MAIN CHAT UI --------
    st.title(f"🤖 Welcome {st.session_state.user} - PDF Chatbot")

    pdf_path = st.text_input("📄 Enter PDF Path (optional):")
    query = st.text_input("❓ Ask Something:")

    if st.button("Send"):

        payload = {"pdf_path": pdf_path, "query": query}

        try:
            r = requests.post(API_URL, json=payload, stream=True)

            # JSON responses (PDF loaded or errors)
            if "application/json" in r.headers.get("content-type", ""):
                data = r.json()
                if "message" in data:
                    st.info(data["message"])
                elif "error" in data:
                    st.error(data["error"])
                st.stop()

            # STREAMING RESPONSE
            st.write("### 🤖 Bot:")

            output_area = st.empty()
            final_text = ""

            for chunk in r.iter_content(chunk_size=50):
                if chunk:
                    txt = chunk.decode()
                    final_text += txt
                    output_area.write(final_text)

            # SAVE TO HISTORY
            st.session_state.history.append({"q": query, "a": final_text})

        except Exception as e:
            st.error(f"API Error: {e}")

    st.stop()



# -------------------------- LOGIN PAGE --------------------------
users = load_users()
st.title("🔐 Login / Sign Up")

option = st.radio("Choose Option", ["Login", "Sign Up"])

# ------------- LOGIN -------------
if option == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.success("Login Successful!")
            st.session_state.logged_in = True
            st.session_state.user = username
            st.rerun()   # <<< FIXED
        else:
            st.error("Incorrect username or password")


# ------------- SIGN UP -------------
if option == "Sign Up":
    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")

    if st.button("Create Account"):
        if new_user in users:
            st.error("Username already exists!")
        else:
            users[new_user] = new_pass
            save_users(users)
            st.success("Account Created! Please login now.")
