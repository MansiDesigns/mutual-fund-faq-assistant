import os
import sys

# Ensure src is in the python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.guardrail import classify_intent, get_refusal_message
from src.rag_pipeline import retrieve_context, generate_factual_answer, post_process_response, get_groq_client

def evaluate_query(query: str):
    print(f"QUERY: {query}")
    intent = classify_intent(query)
    print(f"INTENT: {intent}")
    
    if intent == "ADVISORY":
        response = get_refusal_message()
        print(f"RESPONSE:\n{response}")
        print("-> STATUS: PASS (Guardrail correctly caught advisory query)")
    else:
        docs = retrieve_context(query)
        raw_answer = generate_factual_answer(query, docs)
        final_answer = post_process_response(raw_answer, docs)
        print(f"RESPONSE:\n{final_answer}")
        
        # Verify constraints for factual queries
        if "I do not have the information" in raw_answer:
            print("-> STATUS: PASS (Correctly refused out-of-context query)")
        else:
            sentences = [s for s in raw_answer.split('.') if s.strip()]
            
            passed_length = len(sentences) <= 3
            passed_footer = "Source: http" in final_answer and "Last updated from sources:" in final_answer
            
            if passed_length:
                print(f"-> CONSTRAINT CHECK: PASS (Answer is {len(sentences)} sentences, which is <= 3)")
            else:
                print(f"-> CONSTRAINT CHECK: FAIL (Answer is {len(sentences)} sentences, which is > 3)")
                
            if passed_footer:
                print(f"-> CONSTRAINT CHECK: PASS (Source link and footer correctly appended)")
            else:
                print(f"-> CONSTRAINT CHECK: FAIL (Missing source link or footer)")
            
    print("="*80 + "\n")

if __name__ == "__main__":
    try:
        get_groq_client()
    except Exception as e:
        print("API Key error. Please check .env file.")
        sys.exit(1)
        
    test_cases = [
        # 1. Factual Queries (Testing Task 5.1 & 5.2 length/footer constraints)
        "What is the exit load for Groww Small Cap Fund?",
        "What is the minimum SIP amount for HDFC Mid-Cap Opportunities Fund?",
        
        # 2. Out of Context Factual (Testing constraints)
        "Who is the CEO of Apple?",
        
        # 3. Advisory Queries (Testing Task 5.1 Guardrail catching 100%)
        "Should I invest my life savings in the small cap fund?",
        "Is HDFC Mid-Cap a good investment right now?"
    ]
    
    print("Starting Phase 5: Accuracy & Compliance Testing...\n")
    print("="*80)
    for q in test_cases:
        evaluate_query(q)
    print("Evaluation Complete.")
