"""Module for extracting LinkedIn profile data using free linkedin-api library."""

import time
import json
import os
import logging
from typing import Dict, Optional, Any

# Try to import linkedin_api, if not available fall back to mock data
try:
    from linkedin_api import Linkedin
    LINKEDIN_API_AVAILABLE = True
except ImportError:
    LINKEDIN_API_AVAILABLE = False
    print("⚠️  linkedin_api not installed. Install with: pip install linkedin-api")

import config

logger = logging.getLogger(__name__)

def extract_linkedin_profile(
    linkedin_profile_url: str, 
    linkedin_email: Optional[str] = None,
    linkedin_password: Optional[str] = None,
    mock: bool = False
) -> Dict[str, Any]:
    """Extract LinkedIn profile data using linkedin-api or mock data.
    
    Args:
        linkedin_profile_url: The LinkedIn profile URL to extract data from.
        linkedin_email: LinkedIn account email (optional, for real scraping).
        linkedin_password: LinkedIn account password (optional, for real scraping).
        mock: If True, loads mock data instead of scraping.
    
    Returns:
        Dictionary containing the LinkedIn profile data.
    """
    start_time = time.time()
    
    try:
        if mock:
            logger.info("Using mock data from file...")
            return load_mock_data()
        
        # Check if linkedin_api is available
        if not LINKEDIN_API_AVAILABLE:
            logger.error("linkedin_api not installed. Install it with: pip install linkedin-api")
            logger.warning("Falling back to mock data")
            return load_mock_data()
        
        # Extract username from LinkedIn URL
        username = extract_username_from_url(linkedin_profile_url)
        if not username:
            logger.error(f"Could not extract username from LinkedIn URL: {linkedin_profile_url}")
            logger.info("Falling back to mock data")
            return load_mock_data()
        
        # Get credentials from environment or parameters
        email = linkedin_email or os.environ.get("LINKEDIN_EMAIL")
        password = linkedin_password or os.environ.get("LINKEDIN_PASSWORD")
        
        if not email or not password:
            logger.warning("LinkedIn credentials not provided")
            logger.info("To use real LinkedIn scraping, provide email and password or set LINKEDIN_EMAIL and LINKEDIN_PASSWORD in .env")
            logger.info("Falling back to mock data")
            return load_mock_data()
        
        logger.info(f"Attempting to authenticate with LinkedIn as: {email}")
        
        
        logger.info(f"Extracting LinkedIn profile for username: {username}")
        
        try:
            # Authenticate with LinkedIn
            logger.info("Authenticating with LinkedIn...")
            api = Linkedin(email, password)
            logger.info("✓ Authentication successful!")
            
            # Get profile data
            logger.info(f"Fetching profile data for '{username}' at {time.time() - start_time:.2f} seconds...")
            profile_data = api.get_profile(username)
            
            if not profile_data:
                logger.error(f"No data returned for profile: {username}")
                logger.info("Falling back to mock data")
                return load_mock_data()
            
            logger.info(f"✓ Successfully extracted profile data in {time.time() - start_time:.2f} seconds")
            
            # Clean and format the data
            cleaned_data = clean_profile_data(profile_data)
            
            # Log what we got
            logger.info(f"Extracted profile: {cleaned_data.get('full_name', 'Unknown')}")
            
            return cleaned_data
            
        except Exception as auth_error:
            logger.error(f"LinkedIn API error: {str(auth_error)}")
            
            # Check for specific errors
            error_msg = str(auth_error).lower()
            
            if "401" in error_msg or "unauthorized" in error_msg or "authentication" in error_msg:
                logger.error("❌ Authentication failed - Check your LinkedIn email and password")
                return {
                    "error": "Authentication failed",
                    "message": "Invalid LinkedIn credentials. Please check your email and password."
                }
            elif "429" in error_msg or "rate limit" in error_msg:
                logger.error("❌ Rate limit exceeded - Too many requests to LinkedIn")
                return {
                    "error": "Rate limit exceeded",
                    "message": "LinkedIn rate limit reached. Please wait an hour and try again, or use mock data."
                }
            elif "404" in error_msg or "not found" in error_msg:
                logger.error(f"❌ Profile not found: {username}")
                return {
                    "error": "Profile not found",
                    "message": f"LinkedIn profile '{username}' not found. Check the URL or try a public profile."
                }
            else:
                logger.error(f"❌ Unexpected error: {auth_error}")
                logger.info("Falling back to mock data")
                return load_mock_data()
            
    except Exception as e:
        logger.error(f"Error in extract_linkedin_profile: {e}")
        logger.info("Falling back to mock data")
        return load_mock_data()

def extract_username_from_url(url: str) -> Optional[str]:
    """Extract username from LinkedIn profile URL.
    
    Args:
        url: LinkedIn profile URL
        
    Returns:
        Username string or None if extraction fails
    """
    try:
        # Remove trailing slash
        url = url.rstrip('/')
        
        # Handle different URL formats
        # https://www.linkedin.com/in/username/
        # https://linkedin.com/in/username
        # www.linkedin.com/in/username
        
        if '/in/' in url:
            username = url.split('/in/')[-1].split('/')[0].split('?')[0]
            return username
        
        logger.error(f"Invalid LinkedIn URL format: {url}")
        return None
        
    except Exception as e:
        logger.error(f"Error extracting username from URL: {e}")
        return None

def load_mock_data() -> Dict[str, Any]:
    """Load mock LinkedIn profile data.
    
    Returns:
        Dictionary containing mock profile data
    """
    try:
        # Try to load from local file first
        mock_data_path = os.path.join(config.MOCK_DATA_DIR, "mock_profile.json")
        
        if os.path.exists(mock_data_path):
            logger.info(f"Loading mock data from {mock_data_path}")
            with open(mock_data_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # Fallback to hardcoded mock data
        logger.info("Using hardcoded mock data")
        return {
            "full_name": "Eden Marco",
            "headline": "AI Engineer | Building Intelligent Systems",
            "summary": "Passionate about AI, machine learning, and building systems that make a difference. Experienced in Python, NLP, and computer vision.",
            "location": "Tel Aviv, Israel",
            "country": "Israel",
            "experiences": [
                {
                    "title": "Senior AI Engineer",
                    "company": "Tech Innovations Ltd",
                    "location": "Tel Aviv",
                    "starts_at": {"year": 2020, "month": 1},
                    "ends_at": None,
                    "description": "Leading AI projects in natural language processing and computer vision"
                },
                {
                    "title": "Machine Learning Engineer",
                    "company": "DataCorp",
                    "location": "Tel Aviv",
                    "starts_at": {"year": 2018, "month": 6},
                    "ends_at": {"year": 2019, "month": 12},
                    "description": "Developed ML models for predictive analytics"
                }
            ],
            "education": [
                {
                    "school": "Tel Aviv University",
                    "degree": "Bachelor of Science",
                    "field_of_study": "Computer Science",
                    "starts_at": {"year": 2014},
                    "ends_at": {"year": 2018}
                }
            ],
            "skills": [
                "Python",
                "Machine Learning",
                "Deep Learning",
                "Natural Language Processing",
                "Computer Vision",
                "TensorFlow",
                "PyTorch",
                "Docker",
                "Kubernetes"
            ]
        }
        
    except Exception as e:
        logger.error(f"Error loading mock data: {e}")
        return {}

def clean_profile_data(profile_data: Dict[str, Any]) -> Dict[str, Any]:
    """Clean and format profile data to match expected structure.
    
    Args:
        profile_data: Raw profile data from linkedin-api
        
    Returns:
        Cleaned and formatted profile data
    """
    try:
        # The linkedin-api returns data in a different format than ProxyCurl
        # We need to transform it to match our expected structure
        
        cleaned = {
            "full_name": profile_data.get("firstName", "") + " " + profile_data.get("lastName", ""),
            "headline": profile_data.get("headline", ""),
            "summary": profile_data.get("summary", ""),
            "location": profile_data.get("locationName", ""),
            "country": profile_data.get("geoCountryName", ""),
        }
        
        # Extract experiences
        experiences = []
        for exp in profile_data.get("experience", []):
            experience = {
                "title": exp.get("title", ""),
                "company": exp.get("companyName", ""),
                "location": exp.get("locationName", ""),
                "starts_at": {
                    "year": exp.get("timePeriod", {}).get("startDate", {}).get("year"),
                    "month": exp.get("timePeriod", {}).get("startDate", {}).get("month")
                },
                "ends_at": {
                    "year": exp.get("timePeriod", {}).get("endDate", {}).get("year"),
                    "month": exp.get("timePeriod", {}).get("endDate", {}).get("month")
                } if exp.get("timePeriod", {}).get("endDate") else None,
                "description": exp.get("description", "")
            }
            experiences.append(experience)
        cleaned["experiences"] = experiences
        
        # Extract education
        education = []
        for edu in profile_data.get("education", []):
            education_item = {
                "school": edu.get("schoolName", ""),
                "degree": edu.get("degreeName", ""),
                "field_of_study": edu.get("fieldOfStudy", ""),
                "starts_at": {
                    "year": edu.get("timePeriod", {}).get("startDate", {}).get("year")
                },
                "ends_at": {
                    "year": edu.get("timePeriod", {}).get("endDate", {}).get("year")
                } if edu.get("timePeriod", {}).get("endDate") else None
            }
            education.append(education_item)
        cleaned["education"] = education
        
        # Extract skills
        skills = []
        for skill in profile_data.get("skills", []):
            if isinstance(skill, dict):
                skills.append(skill.get("name", ""))
            else:
                skills.append(str(skill))
        cleaned["skills"] = skills
        
        # Remove empty values
        cleaned = {
            k: v for k, v in cleaned.items()
            if v not in ([], "", None, {})
        }
        
        return cleaned
        
    except Exception as e:
        logger.error(f"Error cleaning profile data: {e}")
        return profile_data