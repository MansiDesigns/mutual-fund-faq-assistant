import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import time

def main():
    print("Initializing embedding model for queries...")
    model_name = "BAAI/bge-small-en-v1.5"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    
    start_time = time.time()
    embedding_model = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    print(f"Model initialized in {time.time() - start_time:.2f} seconds.")

    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chroma_db"))
    print(f"Connecting to ChromaDB at {db_path}...")
    
    # Initialize LangChain's Chroma vector store wrapper
    vector_db = Chroma(
        collection_name="mutual_fund_faqs",
        embedding_function=embedding_model,
        persist_directory=db_path
    )

    # We will test factual queries
    test_queries = [
        "What is the expense ratio of HDFC Mid-Cap Opportunities Fund?",
        "What is the exit load for Groww Small Cap Fund?",
        "What is the minimum SIP amount?"
    ]

    for query in test_queries:
        print("\n" + "="*70)
        print(f"QUERY: {query}")
        print("="*70)
        
        # Retrieve top 3 relevant chunks
        results = vector_db.similarity_search_with_score(query, k=3)
        
        for i, (doc, score) in enumerate(results):
            print(f"\n--- Result {i+1} (Score: {score:.4f}) ---")
            print(f"Source URL: {doc.metadata.get('source_url', 'N/A')}")
            print(f"Last Updated: {doc.metadata.get('last_updated_date', 'N/A')}")
            print(f"Content Snippet: {doc.page_content[:150]}...")

if __name__ == "__main__":
    main()
