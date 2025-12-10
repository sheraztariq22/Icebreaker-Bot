"""
Icebreaker Bot modules package.

This package contains the following modules:
- data_extraction: Functions for extracting LinkedIn profile data
- data_processing: Functions for processing and indexing LinkedIn profile data
- llm_interface: Functions for interfacing with IBM watsonx.ai LLMs
- query_engine: Functions for querying indexed LinkedIn profile data
"""

from modules.data_extraction import extract_linkedin_profile
from modules.data_processing import split_profile_data, create_vector_database, verify_embeddings
from modules.llm_interface import create_watsonx_embedding, create_watsonx_llm, change_llm_model
from modules.query_engine import generate_initial_facts, answer_user_query