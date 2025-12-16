"""Module for querying indexed LinkedIn profile data."""

import logging
from typing import Any, Dict, Optional

from llama_index.core import VectorStoreIndex, PromptTemplate

from modules.llm_interface import get_llm
import config

logger = logging.getLogger(__name__)

def generate_initial_facts(index: VectorStoreIndex) -> str:
    """Generates interesting facts about the person's career or education.
    
    Args:
        index: VectorStoreIndex containing the LinkedIn profile data.
        
    Returns:
        String containing interesting facts about the person.
    """
    try:
        # Get Gemini LLM
        gemini_llm = get_llm()
        
        # Create prompt template
        # Using a default template if not in config
        facts_template = getattr(config, 'INITIAL_FACTS_TEMPLATE', 
            """Context information is below.
---------------------
{context_str}
---------------------
Given the context information and not prior knowledge, provide three interesting facts about this person's career or education.
Be specific and cite actual information from the profile. Keep each fact concise (1-2 sentences).

Facts:
""")
        
        facts_prompt = PromptTemplate(template=facts_template)
        
        # Create query engine
        query_engine = index.as_query_engine(
            streaming=False,
            similarity_top_k=config.SIMILARITY_TOP_K,
            llm=gemini_llm,
            text_qa_template=facts_prompt
        )
        
        # Execute the query
        query = "Provide three interesting facts about this person's career or education. Keep each fact brief."
        response = query_engine.query(query)
        
        # Return the facts
        return response.response
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error in generate_initial_facts: {error_msg}")
        
        # Handle specific error cases
        if "MAX_TOKENS" in error_msg or "terminated early" in error_msg:
            return "Profile processed successfully, but the response was too long. Try asking specific questions in the Chat tab instead."
        elif "RATE_LIMIT" in error_msg or "quota" in error_msg.lower():
            return "Rate limit exceeded. Please wait a moment and try again."
        else:
            return f"Failed to generate initial facts. Error: {error_msg}"

def answer_user_query(index: VectorStoreIndex, user_query: str) -> Any:
    """Answers the user's question using the vector database and the LLM.
    
    Args:
        index: VectorStoreIndex containing the LinkedIn profile data.
        user_query: The user's question.
        
    Returns:
        Response object containing the answer to the user's question.
    """
    try:
        # Get Gemini LLM
        gemini_llm = get_llm()
        
        # Create prompt template
        # Using a default template if not in config
        question_template = getattr(config, 'USER_QUESTION_TEMPLATE',
            """Context information is below.
---------------------
{context_str}
---------------------
Given the context information and not prior knowledge, answer the question: {query_str}

If the answer is not in the context, say "I don't have enough information to answer that question."

Answer:
""")
        
        question_prompt = PromptTemplate(template=question_template)
        
        # Retrieve relevant nodes
        base_retriever = index.as_retriever(similarity_top_k=config.SIMILARITY_TOP_K)
        source_nodes = base_retriever.retrieve(user_query)
        
        # Build context string (for logging/debugging)
        context_str = "\n\n".join([node.node.get_text() for node in source_nodes])
        logger.debug(f"Retrieved {len(source_nodes)} nodes for query: {user_query}")
        
        # Create query engine
        query_engine = index.as_query_engine(
            streaming=False,
            similarity_top_k=config.SIMILARITY_TOP_K,
            llm=gemini_llm,
            text_qa_template=question_prompt
        )
        
        # Execute the query
        answer = query_engine.query(user_query)
        return answer
    except Exception as e:
        logger.error(f"Error in answer_user_query: {e}")
        # Return a simple object with a response attribute for error handling
        class ErrorResponse:
            def __init__(self, message):
                self.response = message
        return ErrorResponse("Failed to get an answer. Please try again.")