import os
import sys

# Ensure we can import from current directory
sys.path.append(os.getcwd())

try:
    print("Importing retriever from vector.py...")
    from vector import retriever
    
    query = "What are the vegan options?"
    print(f"Invoking retriever with query: '{query}'")
    
    docs = retriever.invoke(query)
    
    print(f"Retrieved {len(docs)} documents.")
    for i, doc in enumerate(docs):
        print(f"Rank {i+1}: {doc.page_content[:50]}... (Metadata: {doc.metadata})")
        
    print("\nVerification successful!")

except Exception as e:
    print(f"Verification failed: {e}")
    sys.exit(1)
