from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from src.guardrail import classify_intent, get_refusal_message
from src.rag_pipeline import retrieve_context, generate_factual_answer, post_process_response, get_groq_client

load_dotenv()

app = FastAPI(title="Mutual Fund FAQ API")

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    intent: str

@app.on_event("startup")
async def startup_event():
    # Verify Groq API key is present
    try:
        get_groq_client()
    except Exception as e:
        print(f"Warning: Failed to initialize Groq client on startup: {e}")

@app.post("/query", response_model=QueryResponse)
async def handle_query(request: QueryRequest):
    query = request.query
    
    # 1. Guardrail Intent Classification
    intent = classify_intent(query)
    
    if intent == "ADVISORY":
        return QueryResponse(response=get_refusal_message(), intent=intent)
    
    # 2. RAG Pipeline
    try:
        retrieved_docs = retrieve_context(query)
        raw_answer = generate_factual_answer(query, retrieved_docs)
        response_text = post_process_response(raw_answer, retrieved_docs)
        return QueryResponse(response=response_text, intent=intent)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {e}")

@app.get("/")
async def root():
    return {"message": "Mutual Fund FAQ API is running."}
