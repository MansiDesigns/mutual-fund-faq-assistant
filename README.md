# Mutual Fund FAQ Assistant

A locally-hosted, Retrieval-Augmented Generation (RAG) assistant designed to answer factual questions about Mutual Funds using data exclusively scraped from Groww.

## Architecture Overview

The system is built to strictly adhere to a **facts-only** constraint. It refuses to provide investment advice or opinions.
- **Scraper:** Python `requests` & `BeautifulSoup` to scrape 10 pre-defined mutual fund URLs.
- **Vector Database:** Local `ChromaDB` storing semantic embeddings.
- **Embeddings:** `BAAI/bge-small-en-v1.5` generated via LangChain.
- **LLM:** `qwen/qwen3.8-27b` hosted on Groq for blazing-fast inference.
- **Guardrail:** A lightweight LLM classification step to block advisory queries ("Should I invest?").
- **UI:** Streamlit for a clean, minimal chat interface.

## Setup Instructions

### 1. Prerequisites
Ensure you have Python 3.10+ installed.

### 2. Installation
Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Variables
You must set up your Groq API Key. Open the `.env` file in the root directory and add your key:
```env
GROQ_API_KEY=gsk_your_api_key_here
```

### 4. Running the App
The vector database is pre-populated and committed to the repository (in `chroma_db/`), so you don't need to re-scrape or embed the data.
To launch the Streamlit frontend, simply run:
```bash
streamlit run app.py
```
This will open the assistant in your default web browser (usually at `http://localhost:8501`).

## Known Limitations
- The knowledge base is strictly limited to 10 specific mutual fund URLs. Queries outside these URLs will be rejected with "I do not have the information".
- The system prevents any advisory questions, but extreme edge-case phrasing might occasionally bypass the prompt.
- Streamlit UI state resets upon page refresh.

## Deployment to Streamlit Community Cloud
To make this app public:
1. Initialize a Git repository and commit all files (including the `chroma_db` folder, but **excluding** the `venv` and `.env` files).
2. Push the repository to GitHub.
3. Log into [Streamlit Community Cloud](https://share.streamlit.io/) and create a new app connecting to your repository.
4. In the Streamlit App Settings -> **Secrets**, add your API key:
   ```toml
   GROQ_API_KEY = "gsk_your_api_key_here"
   ```
5. Deploy and share the URL!
