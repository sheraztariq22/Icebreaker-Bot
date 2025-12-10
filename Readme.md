"""Configuration settings for the Icebreaker Bot."""

# IBM watsonx.ai settings
WATSONX_URL = "https://us-south.ml.cloud.ibm.com"
WATSONX_PROJECT_ID = "skills-network"

# Model settings
LLM_MODEL_ID = "ibm/granite-3-2-8b-instruct"
EMBEDDING_MODEL_ID = "ibm/slate-125m-english-rtrvr-v2"

# ProxyCurl API settings
PROXYCURL_API_KEY = ""  # Replace with your API key

# Mock data URL
MOCK_DATA_URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/ZRe59Y_NJyn3hZgnF1iFYA/linkedin-profile-data.json"

# Query settings
SIMILARITY_TOP_K = 5
TEMPERATURE = 0.0
MAX_NEW_TOKENS = 500
MIN_NEW_TOKENS = 1
TOP_K = 50
TOP_P = 1

# Node settings
CHUNK_SIZE = 500

# LLM prompt templates
INITIAL_FACTS_TEMPLATE = """
You are an AI assistant that provides detailed answers based on the provided context.

Context information is below:

{context_str}

Based on the context provided, list 3 interesting facts about this person's career or education.

Answer in detail, using only the information provided in the context.
"""

USER_QUESTION_TEMPLATE = """
You are an AI assistant that provides detailed answers to questions based on the provided context.

Context information is below:

{context_str}

Question: {query_str}

Answer in full details, using only the information provided in the context. If the answer is not available in the context, say "I don't know. The information is not available on the LinkedIn page."
"""
