# Phase-Wise Implementation Plan: Mutual Fund FAQ Assistant

This document outlines the step-by-step implementation strategy for the Mutual Fund FAQ Assistant, based on the approved architecture.

---

## Phase 1: Environment Setup & Data Ingestion (Weeks 1-2)
**Goal:** Successfully scrape, clean, and chunk the factual data from the 10 specified Groww URLs.

*   **Task 1.1: Project Initialization**
    *   Set up the Python virtual environment.
    *   Install core dependencies (`langchain`, `beautifulsoup4`, `chromadb`, `groq`, `streamlit`, etc.).
*   **Task 1.2: Web Scraper Development**
    *   Build a script using `BeautifulSoup` to fetch HTML from the 10 Groww mutual fund URLs.
    *   Ensure the script *only* targets these HTML pages (no PDFs/KIMs).
*   **Task 1.3: Data Cleaning**
    *   Strip out HTML tags, JavaScript, navigation bars, and footers.
    *   Extract only the core text containing scheme details.
*   **Task 1.4: Chunking & Metadata**
    *   Implement `RecursiveCharacterTextSplitter` (e.g., ~500 tokens).
    *   Attach critical metadata to every chunk: `source_url` and `last_updated_date`.

## Phase 2: Vector Storage & Embedding (Week 2)
**Goal:** Convert the scraped text into embeddings and store them for semantic search.

*   **Task 2.1: Embedding Generation**
    *   Initialize the chosen BGE embedding model (e.g., `BAAI/bge-small-en`).
    *   Generate embeddings for all chunks.
*   **Task 2.2: Vector Database Setup**
    *   Initialize local `ChromaDB`.
    *   Insert embeddings and corresponding metadata into the database.
*   **Task 2.3: Retrieval Testing**
    *   Write a basic script to query the database and manually verify that relevant chunks are returned for factual queries (e.g., "expense ratio").

## Phase 3: Core RAG & LLM Integration (Week 3)
**Goal:** Build the logical pipeline that handles classification, retrieval, and strictly formatted generation.

*   **Task 3.1: Query Guardrail (Intent Classifier)**
    *   Implement a lightweight classification step (via LLM or fast classifier) to categorize user input as `FACTUAL` or `ADVISORY`.
    *   Build the **Refusal Handler** to instantly return a hardcoded polite refusal and educational link if `ADVISORY`.
*   **Task 3.2: RAG Pipeline Integration**
    *   Connect the Retriever to the LLM (using Groq, e.g., Llama 3).
    *   Draft the strict System Prompt enforcing: facts only, max 3 sentences, strictly from context.
*   **Task 3.3: Post-Processing module**
    *   Write the function to extract the `source_url` from the retrieved chunk's metadata.
    *   Automatically append the URL and the standard footer (`Last updated from sources: <date>`) to the LLM's raw response.

## Phase 4: User Interface Development (Week 4)
**Goal:** Build a clean, minimal, compliant frontend for users to interact with the assistant.

*   **Task 4.1: Streamlit App Initialization**
    *   Set up a basic chat interface using Streamlit (`st.chat_message`).
*   **Task 4.2: UI Components**
    *   Add the mandatory static Disclaimer: *"Facts-only. No investment advice."* prominently on the screen.
    *   Implement 3 clickable predefined example questions in the sidebar or main screen.
*   **Task 4.3: Backend Integration**
    *   Connect the Streamlit frontend to the Phase 3 RAG pipeline.
    *   Ensure the UI handles and displays the custom footers correctly.

## Phase 5: Testing, Validation & Final Delivery (Week 5)
**Goal:** Ensure the system meets all strict problem statement constraints before handover.

*   **Task 5.1: Accuracy & Compliance Testing**
    *   Test factual queries against known data on the Groww pages.
    *   Aggressively test advisory queries ("Should I buy this?", "Is this a good fund?") to ensure the Guardrail catches 100% of them.
*   **Task 5.2: Constraint Verification**
    *   Verify all generated answers are ≤ 3 sentences.
    *   Verify every answer includes exactly one correct source link and the footer.
*   **Task 5.3: Documentation**
    *   Draft the final `README.md` with setup instructions, architecture overview, and known limitations.
    *   Code cleanup and final delivery.
