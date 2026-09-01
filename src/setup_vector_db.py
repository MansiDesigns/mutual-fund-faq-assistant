import json
import chromadb
import uuid
import os

def main():
    print("Loading data/chunks_with_embeddings.json...")
    if not os.path.exists("data/chunks_with_embeddings.json"):
        print("Error: data/chunks_with_embeddings.json not found. Run generate_embeddings.py first.")
        return

    with open("data/chunks_with_embeddings.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Loaded {len(chunks)} chunks with pre-computed embeddings.")

    # Initialize ChromaDB persistent client
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "chroma_db"))
    print(f"Initializing local ChromaDB at {db_path}...")
    client = chromadb.PersistentClient(path=db_path)
    
    collection_name = "mutual_fund_faqs"
    # Delete collection if exists to avoid duplicates on re-run
    try:
        client.delete_collection(name=collection_name)
        print(f"Deleted existing collection '{collection_name}'.")
    except Exception:
        pass # Collection does not exist
        
    collection = client.create_collection(name=collection_name)

    # Prepare data for insertion
    ids = [str(uuid.uuid4()) for _ in range(len(chunks))]
    embeddings = [c["embedding"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    documents = [c["page_content"] for c in chunks]

    # Insert into Chroma in batches to be safe
    batch_size = 100
    for i in range(0, len(chunks), batch_size):
        end = min(i + batch_size, len(chunks))
        collection.add(
            ids=ids[i:end],
            embeddings=embeddings[i:end],
            metadatas=metadatas[i:end],
            documents=documents[i:end]
        )
        print(f"Inserted batch {i//batch_size + 1} ({end} / {len(chunks)} total).")

    print(f"Successfully inserted {len(chunks)} embeddings into ChromaDB collection '{collection_name}'.")

if __name__ == "__main__":
    main()
