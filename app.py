import streamlit as st
import os
import requests

st.set_page_config(page_title="Mutual Fund FAQ Assistant", page_icon="📈", layout="centered")

st.title("Mutual Fund FAQ Assistant")
st.warning("**Disclaimer:** Facts-only. No investment advice.")

# Retrieve BACKEND_URL from Streamlit Secrets or Environment Variables
# Default to localhost for local testing
try:
    BACKEND_URL = st.secrets.get("BACKEND_URL", os.environ.get("BACKEND_URL", "http://localhost:8000"))
except Exception:
    BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Predefined example questions in sidebar
st.sidebar.title("Example Questions")
example_questions = [
    "What is the expense ratio of HDFC Mid-Cap Opportunities Fund?",
    "What is the minimum SIP amount for Groww Small Cap Fund?",
    "What is the exit load for Parag Parikh Flexi Cap Fund?"
]

# When an example is clicked, update session state variable to trigger chat
for q in example_questions:
    if st.sidebar.button(q):
        st.session_state.example_query = q

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Determine the query (either from chat input or example click)
query = st.chat_input("Ask a factual question about mutual funds...")

if "example_query" in st.session_state and st.session_state.example_query:
    query = st.session_state.example_query
    # Clear it so it doesn't loop
    st.session_state.example_query = None

if query:
    # Display user message in chat message container
    st.chat_message("user").markdown(query)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": query})

    with st.spinner("Asking the assistant..."):
        try:
            res = requests.post(f"{BACKEND_URL}/query", json={"query": query})
            res.raise_for_status()
            data = res.json()
            response = data.get("response", "No response received.")
        except requests.exceptions.RequestException as e:
            response = f"Could not connect to the backend API: {e}\n\nPlease ensure the backend is running and `BACKEND_URL` is set correctly."

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
