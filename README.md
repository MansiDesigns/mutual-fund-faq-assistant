# Mutual Fund FAQ Assistant

A locally-hosted, Retrieval-Augmented Generation (RAG) assistant designed to answer factual questions about Mutual Funds using data exclusively scraped from Groww.

## Architecture Overview

The system is built to strictly adhere to a **facts-only** constraint. It uses a **Client-Server Architecture**:
- **Backend API (FastAPI):** Hosts the RAG pipeline, manages the ChromaDB, and connects to Groq.
- **Frontend UI (Streamlit):** A clean, minimal chat interface that communicates with the backend via HTTP.

Core Components:
- **Scraper:** Python `requests` & `BeautifulSoup` to scrape 10 pre-defined mutual fund URLs.
- **Vector Database:** Local `ChromaDB` storing semantic embeddings.
- **Embeddings:** `BAAI/bge-small-en-v1.5` generated via LangChain.
- **LLM:** `qwen/qwen3.8-27b` hosted on Groq for blazing-fast inference.
- **Guardrail:** A lightweight LLM classification step to block advisory queries ("Should I invest?").

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

### 4. Running the App Locally
The application is decoupled. You need to run both the backend API and the frontend UI.

**Terminal 1 (Backend):**
```bash
uvicorn api:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
streamlit run app.py
```
This will open the assistant in your default web browser (usually at `http://localhost:8501`).

## Known Limitations
- The knowledge base is strictly limited to 10 specific mutual fund URLs. Queries outside these URLs will be rejected with "I do not have the information".
- The system prevents any advisory questions, but extreme edge-case phrasing might occasionally bypass the prompt.
- Streamlit UI state resets upon page refresh.

## Deployment (Railway + Streamlit Cloud)
To make this app public, we deploy the Backend to Railway and the Frontend to Streamlit Community Cloud from the same repository.

### 1. Backend (Railway)
1. Push this repository to your GitHub account.
2. Log into [Railway](https://railway.app/) and create a new project from your GitHub repository.
3. Railway will automatically detect the `Procfile` and deploy the FastAPI server.
4. In the Railway project settings, add the environment variable:
   ```env
   GROQ_API_KEY=gsk_your_api_key_here
   ```
5. Note down the public domain Railway generates for your app (e.g., `https://mutual-fund-faq-production.up.railway.app`).

### 2. Frontend (Streamlit Cloud)
1. Log into [Streamlit Community Cloud](https://share.streamlit.io/) and create a new app connecting to the same repository.
2. In the Streamlit App Settings -> **Secrets**, add your Railway backend URL:
   ```toml
   BACKEND_URL = "https://your-railway-domain.up.railway.app"
   ```
3. Deploy and share the URL!
