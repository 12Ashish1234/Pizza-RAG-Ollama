import sys
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

try:
    import flashrank
    print(f"Flashrank package found: {flashrank.__file__}")
    # Try to access version if available, though some packages don't expose it at top level
    try:
        print(f"Flashrank version: {flashrank.__version__}")
    except AttributeError:
        print("Flashrank version not exposed")
        
    from flashrank import Ranker
    print("Successfully imported Ranker from flashrank")
    
except ImportError as e:
    print(f"Failed to import flashrank: {e}")
except Exception as e:
    print(f"Error with flashrank: {e}")

try:
    from langchain_community.document_compressors.flashrank_rerank import FlashrankRerank
    print("Successfully imported FlashrankRerank from langchain_community")
    
    # Try to instantiate to trigger Pydantic validation
    try:
        compressor = FlashrankRerank()
        print("Successfully instantiated FlashrankRerank")
    except Exception as e:
        print(f"Failed to instantiate FlashrankRerank: {e}")
        
except ImportError as e:
    print(f"Failed to import langchain_community: {e}")
except Exception as e:
    print(f"Error with langchain_community: {e}")
