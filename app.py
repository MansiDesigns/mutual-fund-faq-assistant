import streamlit as st
import os

from src.guardrail import classify_intent, get_refusal_message
from src.rag_pipeline import retrieve_context, generate_factual_answer, post_process_response, get_groq_client

st.set_page_config(page_title="Mutual Fund FAQ Assistant", page_icon="📈", layout="centered")

st.title("Mutual Fund FAQ Assistant")
st.warning("**Disclaimer:** Facts-only. No investment advice.")

# Check API Key
try:
    get_groq_client()
except Exception as e:
    st.error("GROQ_API_KEY is missing or invalid. Please check your `.env` file or Streamlit Secrets.")
    st.stop()

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

    with st.spinner("Classifying and retrieving..."):
        # 1. Guardrail Intent Classification
        intent = classify_intent(query)
        
        if intent == "ADVISORY":
            response = get_refusal_message()
        else:
            # 2. RAG Pipeline
            try:
                retrieved_docs = retrieve_context(query)
                raw_answer = generate_factual_answer(query, retrieved_docs)
                response = post_process_response(raw_answer, retrieved_docs)
            except Exception as e:
                response = f"An error occurred while fetching information: {e}"

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
