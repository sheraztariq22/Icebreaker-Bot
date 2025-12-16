"""Diagnostic script to test ProxyCurl API connection."""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_header(text):
    """Print formatted header."""
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

def test_proxycurl_key():
    """Test ProxyCurl API key."""
    print_header("Testing ProxyCurl API Key")
    
    api_key = os.environ.get("PROXYCURL_API_KEY")
    
    if not api_key:
        print_error("PROXYCURL_API_KEY not found in environment")
        print_info("Set it in your .env file")
        return False
    
    # Check key format
    if api_key == "your_proxycurl_key_here":
        print_error("API key still has placeholder value")
        print_info("Replace with your actual ProxyCurl API key")
        return False
    
    print_success("API key found in environment")
    print_info(f"Key starts with: {api_key[:10]}...")
    
    # Test the key by checking credit balance
    try:
        print_info("Testing API key with credit balance check...")
        
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        response = requests.get(
            "https://nubela.co/proxycurl/api/credit-balance",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            credit_balance = data.get("credit_balance", "Unknown")
            print_success(f"API key is valid!")
            print_info(f"Credit balance: {credit_balance}")
            return True
        elif response.status_code == 401:
            print_error("API key is invalid (401 Unauthorized)")
            print_info("Check your ProxyCurl dashboard for the correct key")
            return False
        elif response.status_code == 403:
            print_error("API key is forbidden (403 Forbidden)")
            print_info("Your account may be inactive or suspended")
            return False
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            print_info(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print_error("Request timed out")
        print_info("Check your internet connection")
        return False
    except requests.exceptions.ConnectionError:
        print_error("Connection error")
        print_info("Check your internet connection")
        return False
    except Exception as e:
        print_error(f"Error testing API key: {e}")
        return False

def test_linkedin_url():
    """Test a LinkedIn URL."""
    print_header("Testing LinkedIn Profile URL")
    
    api_key = os.environ.get("PROXYCURL_API_KEY")
    
    if not api_key or api_key == "your_proxycurl_key_here":
        print_error("Valid ProxyCurl API key needed for this test")
        return False
    
    # Test with a known good profile
    test_url = "https://www.linkedin.com/in/williamhgates/"
    print_info(f"Testing with: {test_url}")
    
    try:
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        
        params = {
            "url": test_url,
            "use_cache": "if-present"
        }
        
        print_info("Sending request to ProxyCurl...")
        
        response = requests.get(
            "https://nubela.co/proxycurl/api/v2/linkedin",
            headers=headers,
            params=params,
            timeout=30
        )
        
        if response.status_code == 200:
            print_success("Successfully retrieved LinkedIn profile!")
            data = response.json()
            print_info(f"Profile: {data.get('full_name', 'Unknown')}")
            print_info(f"Headline: {data.get('headline', 'Unknown')}")
            return True
        elif response.status_code == 404:
            print_error("404 Not Found")
            print_info("This usually means:")
            print_info("  1. The LinkedIn URL format is incorrect")
            print_info("  2. The profile doesn't exist or is private")
            print_info("  3. ProxyCurl endpoint has changed")
            print_info(f"Response: {response.text[:200]}")
            return False
        elif response.status_code == 401:
            print_error("401 Unauthorized - Invalid API key")
            return False
        elif response.status_code == 429:
            print_error("429 Too Many Requests - Rate limit exceeded")
            print_info("Wait a few minutes and try again")
            return False
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            print_info(f"Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print_error(f"Error testing LinkedIn URL: {e}")
        return False

def test_mock_data():
    """Test mock data loading."""
    print_header("Testing Mock Data")
    
    try:
        # Try to load mock data
        mock_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/fad4d7a87e3e934ad52ba2a968bad9eb45128665/eden-marco.json"
        
        print_info("Fetching mock data from GitHub...")
        
        response = requests.get(mock_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Mock data loaded successfully!")
            print_info(f"Profile: {data.get('full_name', 'Unknown')}")
            return True
        else:
            print_error(f"Failed to load mock data: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Error loading mock data: {e}")
        return False

def main():
    """Run all diagnostic tests."""
    print_header("ProxyCurl Diagnostic Tool")
    
    print("This tool will help diagnose ProxyCurl connection issues.")
    print("It will test your API key and connection to ProxyCurl.")
    
    # Test 1: Mock data (should always work)
    mock_result = test_mock_data()
    
    # Test 2: ProxyCurl API key
    key_result = test_proxycurl_key()
    
    # Test 3: LinkedIn profile lookup (only if key is valid)
    url_result = False
    if key_result:
        url_result = test_linkedin_url()
    
    # Summary
    print_header("Diagnostic Summary")
    
    print(f"Mock Data:     {'✓ PASS' if mock_result else '✗ FAIL'}")
    print(f"API Key:       {'✓ PASS' if key_result else '✗ FAIL'}")
    print(f"Profile Lookup: {'✓ PASS' if url_result else '✗ FAIL' if key_result else '⊘ SKIP'}")
    
    print("\n")
    
    if mock_result and not key_result:
        print_info("RECOMMENDATION:")
        print("  - Mock data works fine")
        print("  - ProxyCurl API key issue detected")
        print("  - Use 'Use Mock Data' checkbox in the app for testing")
        print("  - Get a valid ProxyCurl API key from: https://nubela.co/proxycurl")
    elif mock_result and key_result and not url_result:
        print_info("RECOMMENDATION:")
        print("  - API key is valid but profile lookup failed")
        print("  - This might be a temporary ProxyCurl issue")
        print("  - Try again in a few minutes")
        print("  - Or use 'Use Mock Data' for testing")
    elif not mock_result:
        print_error("CRITICAL:")
        print("  - Cannot load mock data")
        print("  - Check your internet connection")
    else:
        print_success("All tests passed! Your setup is working correctly.")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()