import os
from dotenv import load_dotenv
from groq import Groq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

load_dotenv()

_groq_client = None
_vector_db = None

def get_groq_client():
    global _groq_client
    if _groq_client is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            raise ValueError("GROQ_API_KEY is not set or is invalid in .env file.")
        _groq_client = Groq(api_key=api_key)
    return _groq_client

def get_vector_db():
    global _vector_db
    if _vector_db is None:
        db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chroma_db"))
        embedding_model = HuggingFaceBgeEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        _vector_db = Chroma(
            collection_name="mutual_fund_faqs",
            embedding_function=embedding_model,
            persist_directory=db_path
        )
    return _vector_db

def retrieve_context(query: str, k: int = 3):
    """
    Retrieves the top k most relevant chunks from the vector database.
    """
    db = get_vector_db()
    docs = db.similarity_search(query, k=k)
    return docs

def generate_factual_answer(query: str, retrieved_docs: list) -> str:
    """
    Connects the retrieved context to the Groq LLM using a strict System Prompt.
    """
    client = get_groq_client()
    
    # Construct context string
    context_text = "\n\n".join([f"--- Context {i+1} ---\n{doc.page_content}" for i, doc in enumerate(retrieved_docs)])
    
    system_prompt = (
        "You are a highly constrained Mutual Fund FAQ assistant. Your ONLY purpose is to extract factual information "
        "from the provided context and answer the user's query.\n\n"
        "STRICT RULES:\n"
        "1. You must ONLY use the provided context to answer the question. Do not use outside knowledge.\n"
        "2. If the answer is not contained in the context, you MUST say 'I do not have the information to answer that based on the provided context.'\n"
        "3. You MUST keep your answer to a maximum of 3 sentences. Be concise and direct.\n"
        "4. DO NOT provide investment advice, opinions, or performance predictions."
    )
    
    user_prompt = f"Context:\n{context_text}\n\nUser Query: {query}"
    
    try:
        completion = client.chat.completions.create(
            model="qwen/qwen3.8-27b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.0,
            max_tokens=150
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during LLM generation: {e}")
        return "Sorry, I encountered an error while processing your request."

def post_process_response(llm_answer: str, retrieved_docs: list) -> str:
    """
    Extracts the source URL and date from metadata and appends the standard footer.
    """
    # If the LLM refused to answer because it lacked context, do not append a source
    if "I do not have the information" in llm_answer or not retrieved_docs:
        return llm_answer
        
    # Use the top retrieved document as the primary source
    primary_doc = retrieved_docs[0]
    source_url = primary_doc.metadata.get("source_url", "Unknown URL")
    last_updated = primary_doc.metadata.get("last_updated_date", "Unknown Date")
    
    footer = f"\n\nSource: {source_url}\nLast updated from sources: {last_updated}"
    return llm_answer + footer

if __name__ == "__main__":
    test_queries = [
        "What is the minimum SIP amount for HDFC Mid-Cap Opportunities Fund?",
        "What is the exit load for Groww Small Cap Fund?",
        "Who won the cricket world cup?" # Out of context query
    ]
    
    print("Testing RAG Pipeline Integration...\n")
    try:
        get_groq_client()
        for q in test_queries:
            print(f"QUERY: {q}")
            docs = retrieve_context(q)
            print("Retrieved Context: (Snippets)")
            for i, d in enumerate(docs):
                print(f"  [{i+1}] {d.page_content[:60]}...")
            
            answer = generate_factual_answer(q, docs)
            final_answer = post_process_response(answer, docs)
            print(f"\nFINAL ANSWER:\n{final_answer}\n")
            print("="*60 + "\n")
    except ValueError as e:
        print(e)
