import sys
import os

# Get the absolute path to the 'enterprise-rag' root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.append(root_path)

import streamlit as st
from app.main import run_chatbot  # Now Python can find this
from app.auth import login

# Ensure the parent directory is in the path for custom module imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Placeholder imports - Replace these with your actual backend logic
# from backend_module import login, run_chatbot 

# Page Configuration
st.set_page_config(page_title="Enterprise AI Knowledge Chatbot", layout="wide")
st.title("🚀 Enterprise AI Knowledge Chatbot")

# Create documents directory if it doesn't exist
if not os.path.exists("documents"):
    os.makedirs("documents")

# --- Session State Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

# --- Login Logic ---
if not st.session_state.logged_in:
    st.subheader("Login to Access Knowledge Base")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            # Assuming login() is defined in your imported backend
            if 'login' in globals() and login(username.strip(), password.strip()):
                st.session_state.logged_in = True
                st.success("Login Successful ✅")
                st.rerun()
            elif username == "admin" and password == "1234": # Temp bypass for testing
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid username or password ❌")

# --- Main App Interface ---
if st.session_state.logged_in:
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))
    
    st.subheader("📄 Step 1: Upload Company Document")
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    if uploaded_file:
        file_path = os.path.join("documents", uploaded_file.name)
        
        # Save file to disk
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.info(f"Processing {uploaded_file.name}...")

        # Initialize the QA Chain only if it hasn't been done or file changed
        if st.session_state.qa_chain is None:
            # run_chatbot should return your LangChain / LLM object
            with st.spinner("Indexing document..."):
                st.session_state.qa_chain = run_chatbot(file_path)
            st.success("📄 File processed and indexed! ✅")

    # Chat Interface
    if st.session_state.qa_chain:
        st.divider()
        st.subheader("💬 Step 2: Ask your question")
        query = st.text_input("What would you like to know from the document?")

        if query:
            with st.spinner("Generating response..."):
                # Using the stored chain to avoid re-indexing the PDF
                response = st.session_state.qa_chain.run(query)
                
                # Cleaning the response
                clean_response = response.strip()
                if clean_response.lower().startswith(query.lower()):
                    clean_response = clean_response[len(query):].strip()

                st.chat_message("assistant").write(clean_response)