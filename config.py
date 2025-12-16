"""Configuration file for the Icebreaker Bot with Google Gemini."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# Google Gemini Configuration
# ============================================================================

# Get Gemini API key from environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Gemini model to use for chat/generation
# Options: 
#   - "gemini-2.5-flash" (Recommended - Fast, efficient, latest)
#   - "gemini-2.5-pro" (Most capable, more expensive)
#   - "gemini-1.5-flash" (Good balance, previous generation)
#   - "gemini-1.5-pro" (Capable, previous generation)
LLM_MODEL_ID = "gemini-2.5-flash"

# Gemini embedding model
# Options:
#   - "models/text-embedding-004" (Latest, recommended)
#   - "models/embedding-001" (Older version)
EMBEDDING_MODEL = "models/text-embedding-004"

# ============================================================================
# LLM Parameters
# ============================================================================

# Temperature for generation (0.0-1.0)
# Lower = more deterministic, Higher = more creative
LLM_TEMPERATURE = 0.7

# Maximum tokens to generate
MAX_TOKENS = 1024

# Top-p sampling (0.0-1.0)
TOP_P = 0.95

# Top-k sampling
TOP_K = 40

# ============================================================================
# ProxyCurl Configuration (LinkedIn Scraping)
# ============================================================================

# ProxyCurl API key for LinkedIn profile extraction
PROXYCURL_API_KEY = os.environ.get("PROXYCURL_API_KEY")

# ProxyCurl API endpoint
PROXYCURL_API_ENDPOINT = "https://nubela.co/proxycurl/api/v2/linkedin"

# ============================================================================
# Vector Database Configuration
# ============================================================================

# Chunk size for splitting profile data
CHUNK_SIZE = 512

# Chunk overlap for better context
CHUNK_OVERLAP = 50

# Number of similar chunks to retrieve
SIMILARITY_TOP_K = 3

# ============================================================================
# Application Configuration
# ============================================================================

# Directory for storing mock data
MOCK_DATA_DIR = "mock_data"

# Mock data URL (fallback if local file not found)
MOCK_DATA_URL = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"

# Logging level
LOG_LEVEL = "INFO"

# ============================================================================
# Prompt Templates
# ============================================================================

# Template for generating initial facts about a profile
INITIAL_FACTS_TEMPLATE = """Context information is below.
---------------------
{context_str}
---------------------
Given the context information and not prior knowledge, provide three interesting and specific facts about this person's career or education.
Be detailed and cite actual information from the profile.

Format your response as:
1. [First fact]
2. [Second fact]
3. [Third fact]

Facts:
"""

# Template for answering user questions about a profile
USER_QUESTION_TEMPLATE = """Context information is below.
---------------------
{context_str}
---------------------
Given the context information and not prior knowledge, answer the question: {query_str}

If the answer is not in the context, say "I don't have enough information to answer that question based on the profile."

Provide a clear, concise answer based only on the information provided.

Answer:
"""

# ============================================================================
# Validation
# ============================================================================

def validate_config():
    """Validate that required configuration is present."""
    if not GEMINI_API_KEY:
        print("WARNING: GEMINI_API_KEY is not set in environment variables.")
        print("Please set it in your .env file or as an environment variable.")
        print("You can get a free API key from: https://aistudio.google.com/app/apikey")
    
    if not PROXYCURL_API_KEY:
        print("INFO: PROXYCURL_API_KEY is not set. You can use mock data for testing.")
    
    return bool(GEMINI_API_KEY)

# Run validation on import
if __name__ == "__main__":
    validate_config()