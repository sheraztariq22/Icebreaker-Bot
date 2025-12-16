"""LLM interface module using Google Gemini API."""

import os
import logging
from typing import Optional

# LlamaIndex imports for Gemini
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import Settings

import config

# Set up logging
logger = logging.getLogger(__name__)

# Global variables to store the current LLM and embedding model
_current_llm = None
_current_embed_model = None

def initialize_gemini_models(
    model_id: Optional[str] = None,
    embedding_model: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
) -> tuple:
    """
    Initialize Google Gemini LLM and embedding models.
    
    Args:
        model_id: Gemini model ID (e.g., "gemini-2.5-flash")
        embedding_model: Gemini embedding model (e.g., "models/text-embedding-004")
        api_key: Google API key (uses environment variable if not provided)
        temperature: Generation temperature (0.0-1.0)
        max_tokens: Maximum tokens to generate
        
    Returns:
        tuple: (llm, embed_model) instances
    """
    global _current_llm, _current_embed_model
    
    # Use defaults from config if not provided
    model_id = model_id or config.LLM_MODEL_ID
    embedding_model = embedding_model or config.EMBEDDING_MODEL
    api_key = api_key or config.GEMINI_API_KEY
    temperature = temperature if temperature is not None else config.LLM_TEMPERATURE
    max_tokens = max_tokens or config.MAX_TOKENS
    
    if not api_key:
        raise ValueError(
            "Gemini API key is required. Please set GEMINI_API_KEY in your .env file "
            "or pass it as an argument. Get a free key at: https://aistudio.google.com/app/apikey"
        )
    
    try:
        logger.info(f"Initializing Gemini LLM with model: {model_id}")
        
        # Initialize Gemini LLM
        llm = GoogleGenAI(
            model=model_id,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        logger.info(f"Initializing Gemini Embedding model: {embedding_model}")
        
        # Initialize Gemini Embedding model
        embed_model = GoogleGenAIEmbedding(
            model_name=embedding_model,
            api_key=api_key,
        )
        
        # Set global models in LlamaIndex Settings
        Settings.llm = llm
        Settings.embed_model = embed_model
        Settings.chunk_size = config.CHUNK_SIZE
        Settings.chunk_overlap = config.CHUNK_OVERLAP
        
        # Store globally for reference
        _current_llm = llm
        _current_embed_model = embed_model
        
        logger.info("Successfully initialized Gemini models")
        
        return llm, embed_model
        
    except Exception as e:
        logger.error(f"Failed to initialize Gemini models: {e}")
        raise

def get_llm():
    """
    Get the current LLM instance.
    Initializes if not already initialized.
    
    Returns:
        GoogleGenAI: Current LLM instance
    """
    global _current_llm
    
    if _current_llm is None:
        logger.info("LLM not initialized, initializing now...")
        initialize_gemini_models()
    
    return _current_llm

def get_embed_model():
    """
    Get the current embedding model instance.
    Initializes if not already initialized.
    
    Returns:
        GoogleGenAIEmbedding: Current embedding model instance
    """
    global _current_embed_model
    
    if _current_embed_model is None:
        logger.info("Embedding model not initialized, initializing now...")
        initialize_gemini_models()
    
    return _current_embed_model

def change_llm_model(model_id: str):
    """
    Change the current LLM model.
    
    Args:
        model_id: New Gemini model ID to use
    """
    global _current_llm
    
    logger.info(f"Changing LLM model to: {model_id}")
    
    try:
        # Create new LLM with the specified model
        llm = GoogleGenAI(
            model=model_id,
            api_key=config.GEMINI_API_KEY,
            temperature=config.LLM_TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
        )
        
        # Update global settings
        Settings.llm = llm
        _current_llm = llm
        
        logger.info(f"Successfully changed LLM model to: {model_id}")
        
    except Exception as e:
        logger.error(f"Failed to change LLM model: {e}")
        raise

def test_gemini_connection():
    """
    Test the connection to Gemini API.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        llm = get_llm()
        
        # Test with a simple prompt
        response = llm.complete("Say 'Hello' in one word.")
        
        logger.info(f"Gemini connection test successful. Response: {response.text}")
        return True
        
    except Exception as e:
        logger.error(f"Gemini connection test failed: {e}")
        return False

# Initialize models on module import
try:
    if config.GEMINI_API_KEY:
        initialize_gemini_models()
        logger.info("Gemini models initialized successfully on import")
    else:
        logger.warning("GEMINI_API_KEY not found. Models will be initialized on first use.")
except Exception as e:
    logger.warning(f"Could not initialize models on import: {e}")