"""Module for extracting LinkedIn profile data."""

import time
import requests
import logging
import json
import os
from typing import Dict, Optional, Any

import config

logger = logging.getLogger(__name__)

def extract_linkedin_profile(
    linkedin_profile_url: str, 
    api_key: Optional[str] = None, 
    mock: bool = False
) -> Dict[str, Any]:
    """Extract LinkedIn profile data using ProxyCurl API or loads a premade JSON file.
    
    Args:
        linkedin_profile_url: The LinkedIn profile URL to extract data from.
        api_key: ProxyCurl API key. Required if mock is False.
        mock: If True, loads mock data from a premade JSON file instead of using the API.
    
    Returns:
        Dictionary containing the LinkedIn profile data.
    """
    start_time = time.time()
    
    try:
        if mock:
            logger.info("Using mock data from a premade JSON file...")
            
            # Try to load from local file first
            mock_data_path = os.path.join(config.MOCK_DATA_DIR, "mock_profile.json")
            
            if os.path.exists(mock_data_path):
                logger.info(f"Loading mock data from {mock_data_path}")
                with open(mock_data_path, 'r') as f:
                    data = json.load(f)
            else:
                # Fallback to URL if local file doesn't exist
                logger.info("Local mock file not found, trying URL...")
                mock_url = getattr(config, 'MOCK_DATA_URL', 
                    "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json")
                response = requests.get(mock_url, timeout=30)
                response.raise_for_status()
                data = response.json()
        else:
            # Ensure API key is provided when mock is False
            if not api_key:
                raise ValueError("ProxyCurl API key is required when mock is set to False.")
            
            logger.info("Starting to extract the LinkedIn profile...")
            
            # Validate and clean the LinkedIn URL
            linkedin_profile_url = linkedin_profile_url.strip()
            if not linkedin_profile_url.startswith("http"):
                linkedin_profile_url = "https://" + linkedin_profile_url
            
            logger.info(f"Processing LinkedIn URL: {linkedin_profile_url}")
            
            # Set up the API endpoint and headers
            # ProxyCurl uses v2 endpoint
            api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            
            # Prepare parameters for the request
            params = {
                "url": linkedin_profile_url,
                "fallback_to_cache": "on-error",
                "use_cache": "if-present",
                "skills": "include",
                "inferred_salary": "include",
                "personal_email": "include",
                "personal_contact_number": "include"
            }
            
            logger.info(f"Sending API request to ProxyCurl at {time.time() - start_time:.2f} seconds...")
            logger.info(f"API Endpoint: {api_endpoint}")
            
            # Send API request
            response = requests.get(api_endpoint, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
        
        logger.info(f"Received response at {time.time() - start_time:.2f} seconds...")
        
        # Clean the data, remove empty values and unwanted fields
        data = {
            k: v
            for k, v in data.items()
            if v not in ([], "", None) and k not in ["people_also_viewed", "certifications"]
        }
        
        # Remove profile picture URLs from groups to clean the data
        if data.get("groups"):
            for group_dict in data.get("groups"):
                group_dict.pop("profile_pic_url", None)
        
        logger.info(f"Successfully extracted profile data in {time.time() - start_time:.2f} seconds")
        return data
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Request error in extract_linkedin_profile: {e}")
        return {}
    except ValueError as e:
        logger.error(f"JSON parsing error: {e}")
        return {}
    except Exception as e:
        logger.error(f"Error in extract_linkedin_profile: {e}")
        return {}