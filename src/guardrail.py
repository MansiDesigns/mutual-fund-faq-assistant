import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv()

# We will lazily initialize the Groq client
_client = None

def get_groq_client():
    global _client
    if _client is None:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key or api_key == "your_groq_api_key_here":
            raise ValueError("GROQ_API_KEY is not set or is invalid in .env file.")
        _client = Groq(api_key=api_key)
    return _client

def classify_intent(query: str) -> str:
    """
    Categorizes the user input as FACTUAL or ADVISORY using a lightweight LLM call.
    """
    prompt = f"""
    You are an intent classifier for a Mutual Fund FAQ Assistant. 
    Classify the following query as either 'FACTUAL' or 'ADVISORY'.
    
    FACTUAL: Queries asking for objective data, definitions, processes, NAV, expense ratios, minimum amounts, exit loads, etc.
    ADVISORY: Queries asking for opinions, recommendations, performance comparisons, or investment advice (e.g., "Should I invest?", "Which is better?", "Is this a good fund?").
    
    Query: "{query}"
    
    Respond ONLY with the exact word FACTUAL or ADVISORY. Do not include any other text.
    """
    
    try:
        client = get_groq_client()
        completion = client.chat.completions.create(
            model="qwen/qwen3.8-27b", 
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
            max_tokens=10
        )
        
        intent = completion.choices[0].message.content.strip().upper()
        if "ADVISORY" in intent:
            return "ADVISORY"
        return "FACTUAL"
    except Exception as e:
        print(f"Error during classification: {e}")
        # Default to FACTUAL, or raise error. 
        # In production, we might want to fail safe or alert.
        return "FACTUAL"

def get_refusal_message() -> str:
    """
    Returns a hardcoded polite refusal and educational link for advisory queries.
    """
    return (
        "I can only provide factual information about mutual funds. I cannot offer investment advice, "
        "opinions, or recommendations on what to buy or sell.\n\n"
        "For educational resources and general guidance, please visit the official "
        "[AMFI Investor Corner](https://www.amfiindia.com/investor-corner) or the "
        "[SEBI Investor Website](https://investor.sebi.gov.in/)."
    )

if __name__ == "__main__":
    # Test cases to run manually once a valid API key is in .env
    queries = [
        "What is the expense ratio for HDFC Flexi Cap?",
        "Should I invest my money in Groww Small Cap fund?",
        "Which fund gives the best returns?"
    ]
    
    print("Testing Guardrail Intent Classifier...\n")
    try:
        get_groq_client() # Check if key is valid before testing
        for q in queries:
            intent = classify_intent(q)
            print(f"Query: {q}")
            print(f"Intent: {intent}")
            if intent == "ADVISORY":
                print(f"Response: {get_refusal_message()}")
            print("-" * 50)
    except ValueError as e:
        print(e)
        print("Please add a valid Groq API key to the .env file to run these tests.")
