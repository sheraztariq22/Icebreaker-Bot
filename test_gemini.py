"""Test script to verify Google Gemini integration."""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_header(text):
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_success(text):
    """Print success message."""
    print(f"✓ {text}")

def print_error(text):
    """Print error message."""
    print(f"✗ {text}")

def print_info(text):
    """Print info message."""
    print(f"ℹ {text}")

def test_environment():
    """Test environment setup."""
    print_header("Testing Environment Setup")
    
    # Check Python version
    python_version = sys.version_info
    print_info(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version >= (3, 9):
        print_success("Python version is 3.9 or higher")
    else:
        print_error("Python 3.9+ is required")
        return False
    
    # Check for API key
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key and api_key != "your_gemini_api_key_here":
        print_success("GEMINI_API_KEY is set")
    else:
        print_error("GEMINI_API_KEY is not set or still has placeholder value")
        print_info("Get a free API key from: https://aistudio.google.com/app/apikey")
        return False
    
    return True

def test_imports():
    """Test that all required packages are installed."""
    print_header("Testing Package Imports")
    
    packages = {
        "google.genai": "google-genai",
        "llama_index.llms.google_genai": "llama-index-llms-google-genai",
        "llama_index.embeddings.google_genai": "llama-index-embeddings-google-genai",
        "llama_index.core": "llama-index",
        "gradio": "gradio",
        "dotenv": "python-dotenv",
    }
    
    all_imported = True
    for module, package in packages.items():
        try:
            __import__(module)
            print_success(f"{package} installed")
        except ImportError as e:
            print_error(f"{package} not installed: {e}")
            all_imported = False
    
    return all_imported

def test_gemini_connection():
    """Test connection to Gemini API."""
    print_header("Testing Gemini API Connection")
    
    try:
        from llama_index.llms.google_genai import GoogleGenAI
        
        # Initialize LLM
        llm = GoogleGenAI(
            model="gemini-2.5-flash",
            api_key=os.environ.get("GEMINI_API_KEY"),
        )
        
        print_info("Sending test prompt to Gemini...")
        
        # Test with a simple prompt
        response = llm.complete("Say 'Hello' in one word.")
        
        print_success("Gemini API connection successful")
        print_info(f"Response: {response.text}")
        
        return True
        
    except Exception as e:
        print_error(f"Gemini API connection failed: {e}")
        return False

def test_gemini_embedding():
    """Test Gemini embedding model."""
    print_header("Testing Gemini Embedding Model")
    
    try:
        from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
        
        # Initialize embedding model
        embed_model = GoogleGenAIEmbedding(
            model_name="models/text-embedding-004",
            api_key=os.environ.get("GEMINI_API_KEY"),
        )
        
        print_info("Generating test embeddings...")
        
        # Test embedding generation
        text = "This is a test sentence for embedding."
        embedding = embed_model.get_text_embedding(text)
        
        print_success("Embedding generation successful")
        print_info(f"Embedding dimension: {len(embedding)}")
        print_info(f"First 5 values: {embedding[:5]}")
        
        return True
        
    except Exception as e:
        print_error(f"Embedding generation failed: {e}")
        return False

def test_config():
    """Test configuration module."""
    print_header("Testing Configuration")
    
    try:
        import config
        
        print_info(f"LLM Model: {config.LLM_MODEL_ID}")
        print_info(f"Embedding Model: {config.EMBEDDING_MODEL}")
        print_info(f"Temperature: {config.LLM_TEMPERATURE}")
        print_info(f"Max Tokens: {config.MAX_TOKENS}")
        print_info(f"Chunk Size: {config.CHUNK_SIZE}")
        
        if config.validate_config():
            print_success("Configuration is valid")
            return True
        else:
            print_error("Configuration validation failed")
            return False
            
    except Exception as e:
        print_error(f"Configuration test failed: {e}")
        return False

def test_llm_interface():
    """Test LLM interface module."""
    print_header("Testing LLM Interface")
    
    try:
        from modules.llm_interface import test_gemini_connection
        
        if test_gemini_connection():
            print_success("LLM interface is working")
            return True
        else:
            print_error("LLM interface test failed")
            return False
            
    except Exception as e:
        print_error(f"LLM interface test failed: {e}")
        return False

def main():
    """Run all tests."""
    print_header("LinkedIn Icebreaker Bot - Gemini Integration Tests")
    
    tests = [
        ("Environment Setup", test_environment),
        ("Package Imports", test_imports),
        ("Configuration", test_config),
        ("Gemini API Connection", test_gemini_connection),
        ("Gemini Embeddings", test_gemini_embedding),
        ("LLM Interface", test_llm_interface),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Print summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("\nAll tests passed! Your Gemini integration is ready.")
        print_info("\nNext steps:")
        print_info("1. Run the app: python app.py")
        print_info("2. Test with mock data first")
        print_info("3. Then try with real LinkedIn profiles")
        return True
    else:
        print_error("\nSome tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)