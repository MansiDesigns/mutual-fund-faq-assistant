# Evaluation Strategy (Eval.md)

This document outlines the evaluation criteria, metrics, and checks for each phase of the project as defined in the `implementation_plan.md`. The goal is to ensure strict adherence to the problem statement constraints at every step of development.

---

## Phase 1: Environment Setup & Data Ingestion

**Objective:** Ensure high-quality, clean, and properly chunked data from the 10 selected Groww URLs.

### Evaluation Criteria
*   **Data Completeness:** 100% of the text relating to the scheme's core facts (Expense Ratio, Exit Load, AUM, Lock-in, etc.) must be successfully scraped.
*   **Data Cleanliness:** 0% presence of HTML tags, JavaScript blobs, promotional banners, or irrelevant navigation links in the final text.
*   **Metadata Integrity:** 100% of generated chunks must contain valid `source_url` and `last_updated_date` metadata.
*   **Chunk Distribution:** Chunks should roughly adhere to the ~500 token limit. No empty or single-word chunks should exist.

### How to Evaluate
1.  Manually inspect a random sample of 20 text chunks.
2.  Write a script to assert that every single chunk in the dataset has a non-null `source_url`.

---

## Phase 2: Vector Storage & Embedding

**Objective:** Verify that the BGE embedding model accurately represents the text and ChromaDB successfully retrieves relevant chunks.

### Evaluation Criteria
*   **Storage Success:** The number of vectors in ChromaDB should exactly match the number of text chunks generated in Phase 1.
*   **Basic Retrieval (Recall@K):** Given a factual query, the most relevant chunk containing the answer should appear in the Top-3 retrieved results.

### How to Evaluate
1.  Query the ChromaDB collection count and compare it against the chunk list length.
2.  Run a set of 10 test queries (e.g., *"What is the benchmark index for Groww Small Cap?"*) bypassing the LLM, and manually verify that the Top-3 returned chunks contain the factual answer.

---

## Phase 3: Core RAG & LLM Integration

**Objective:** Validate the Guardrail (Intent Classifier), LLM adherence to facts, and Post-Processor formatting.

### Evaluation Criteria
*   **Guardrail Accuracy:** 
    *   **Advisory Queries:** 100% must be caught and routed to the Refusal Handler. False negatives (giving advice) are unacceptable.
    *   **Factual Queries:** High pass-through rate. False positives (refusing to answer a valid factual question) should be minimized (< 5%).
*   **LLM Hallucination Rate:** 0%. The Groq (Llama 3) LLM must strictly synthesize answers from the provided context only.
*   **Post-Processor Formatting:** 100% of factual responses must end with exactly one citation link and the standard footer.

### How to Evaluate
1.  **Red-teaming the Guardrail:** Feed a test suite of 30 queries (15 explicitly factual, 15 cleverly disguised advisory queries) and assert the classification routing.
2.  **Context-bound Testing:** Ask the LLM a factual question *about a fund not in the corpus*. The expected behavior is for the LLM to admit it doesn't know, not hallucinate an answer.
3.  **Regex Check:** Use regex on the final output string to ensure `\n\nSource: https://...` and `Last updated from sources: ...` are perfectly formatted.

---

## Phase 4: User Interface Development

**Objective:** Ensure the Streamlit interface is minimal, compliant, and privacy-first.

### Evaluation Criteria
*   **Visual Constraints:** The static disclaimer (*"Facts-only. No investment advice."*) must be continuously visible.
*   **Interactivity:** The 3 predefined example questions must successfully trigger the RAG pipeline when clicked.
*   **Privacy Verification:** No code in the Streamlit app should attempt to capture, log, or persist user sessions, IP addresses, or PII.

### How to Evaluate
1.  **Manual UI Walkthrough:** Load the app locally. Click all example questions. Resize the window to ensure the disclaimer remains visible.
2.  **Code Review:** Inspect `app.py` (or equivalent) to ensure no state persistence or logging mechanisms for user identities exist.

---

## Phase 5: Testing, Validation & Final Delivery

**Objective:** End-to-End (E2E) verification of the entire system against the strictest problem statement rules.

### Evaluation Criteria
*   **Length Constraint:** 100% of factual answers must be ≤ 3 sentences.
*   **E2E Latency:** Because Groq is being used, generation should be nearly instantaneous. Overall system latency (Classification -> Retrieval -> Generation -> UI) should ideally be under 2 seconds.

### How to Evaluate
1.  **Automated E2E Suite:** Run an automated script simulating a user asking 50 diverse factual questions.
2.  **Sentence Counting:** Use NLP (e.g., `nltk.sent_tokenize`) to programmatically assert that the length of the generated response (excluding the footer) never exceeds 3 sentences for all 50 test cases.
3.  **Final Code Audit:** Ensure the `README.md` is complete and accurately reflects the local setup instructions.
