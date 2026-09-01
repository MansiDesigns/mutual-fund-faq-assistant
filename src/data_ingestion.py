import requests
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from datetime import datetime
import json
import os

URLS = [
    "https://groww.in/mutual-funds/hdfc-mid-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/hdfc-equity-fund-direct-growth",
    "https://groww.in/mutual-funds/hdfc-focused-fund-direct-growth",
    "https://groww.in/mutual-funds/hdfc-elss-tax-saver-fund-direct-plan-growth",
    "https://groww.in/mutual-funds/hdfc-large-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/groww-multicap-fund-direct-growth",
    "https://groww.in/mutual-funds/groww-silver-etf-fof-direct-growth",
    "https://groww.in/mutual-funds/groww-small-cap-fund-direct-growth",
    "https://groww.in/mutual-funds/groww-gold-etf-fof-direct-growth",
    "https://groww.in/mutual-funds/amc/groww-mutual-funds"
]

def fetch_html(url):
    """Fetches HTML content from a given URL."""
    print(f"Fetching: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def clean_html(html_content):
    """Cleans HTML content to extract core text."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted tags
    for element in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        element.decompose()
        
    # Extract text and collapse multiple newlines/spaces
    text = soup.get_text(separator=' ')
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    cleaned_text = '\n'.join(chunk for chunk in chunks if chunk)
    return cleaned_text

def chunk_text(text, url):
    """Splits text into chunks and attaches metadata."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = splitter.split_text(text)
    
    documents = []
    current_date = datetime.now().strftime("%Y-%m-%d")
    for chunk in chunks:
        doc = Document(
            page_content=chunk,
            metadata={
                "source_url": url,
                "last_updated_date": current_date
            }
        )
        documents.append(doc)
    return documents

def process_urls(urls):
    """Processes all URLs and returns a list of Document objects."""
    all_documents = []
    for url in urls:
        try:
            html = fetch_html(url)
            clean_txt = clean_html(html)
            docs = chunk_text(clean_txt, url)
            all_documents.extend(docs)
            print(f"Successfully processed {url}, extracted {len(docs)} chunks.")
        except Exception as e:
            print(f"Error processing {url}: {e}")
    return all_documents

if __name__ == "__main__":
    docs = process_urls(URLS)
    print(f"Total chunks extracted: {len(docs)}")
    
    # Optionally save to a file for verification in Phase 1
    os.makedirs("data", exist_ok=True)
    with open("data/chunks.json", "w", encoding="utf-8") as f:
        json_docs = [{"page_content": d.page_content, "metadata": d.metadata} for d in docs]
        json.dump(json_docs, f, indent=2, ensure_ascii=False)
    print("Chunks saved to data/chunks.json")
