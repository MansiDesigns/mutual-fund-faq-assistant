import json
import os
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import time

def main():
    print("Loading chunks from data/chunks.json...")
    if not os.path.exists("data/chunks.json"):
        print("Error: data/chunks.json not found. Please run data_ingestion.py first.")
        return

    with open("data/chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)
    
    print(f"Loaded {len(chunks)} chunks.")

    print("Initializing BGE embedding model (BAAI/bge-small-en-v1.5)...")
    model_name = "BAAI/bge-small-en-v1.5"
    model_kwargs = {'device': 'cpu'} # Use CPU to ensure compatibility everywhere
    encode_kwargs = {'normalize_embeddings': True} # Good practice for BGE models
    
    start_time = time.time()
    embedding_model = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    print(f"Model initialized in {time.time() - start_time:.2f} seconds.")
    
    print("Generating embeddings for all chunks... (This may take a minute)")
    texts = [chunk["page_content"] for chunk in chunks]
    
    start_time = time.time()
    embeddings = embedding_model.embed_documents(texts)
    print(f"Successfully generated {len(embeddings)} embeddings of dimension {len(embeddings[0])} in {time.time() - start_time:.2f} seconds.")
    
    # Save the embeddings along with the chunks for verification
    for i, chunk in enumerate(chunks):
        chunk["embedding"] = embeddings[i]
        
    with open("data/chunks_with_embeddings.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f)
        
    print("Embeddings generated and saved to data/chunks_with_embeddings.json.")

if __name__ == "__main__":
    main()
