"""Test script to verify LinkedIn authentication and scraping."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def print_success(text):
    print(f"✓ {text}")

def print_error(text):
    print(f"✗ {text}")

def print_info(text):
    print(f"ℹ {text}")

def test_linkedin_api_import():
    """Test if linkedin-api is installed."""
    print_header("Step 1: Testing linkedin-api Installation")
    
    try:
        from linkedin_api import Linkedin
        print_success("linkedin-api is installed")
        return True
    except ImportError:
        print_error("linkedin-api is NOT installed")
        print_info("Install it with: pip install linkedin-api")
        return False

def test_credentials():
    """Test if credentials are available."""
    print_header("Step 2: Checking LinkedIn Credentials")
    
    email = os.environ.get("LINKEDIN_EMAIL")
    password = os.environ.get("LINKEDIN_PASSWORD")
    
    if not email:
        print_error("LINKEDIN_EMAIL not found in .env")
        return None, None
    
    if not password:
        print_error("LINKEDIN_PASSWORD not found in .env")
        return None, None
    
    print_success("LinkedIn email found")
    print_info(f"Email: {email}")
    print_success("LinkedIn password found")
    print_info(f"Password: {'*' * len(password)}")
    
    return email, password

def test_authentication(email, password):
    """Test LinkedIn authentication."""
    print_header("Step 3: Testing LinkedIn Authentication")
    
    if not email or not password:
        print_error("Cannot test without credentials")
        return False
    
    try:
        from linkedin_api import Linkedin
        
        print_info("Attempting to authenticate...")
        api = Linkedin(email, password)
        
        print_success("✓ Authentication successful!")
        return api
        
    except Exception as e:
        print_error(f"Authentication failed: {e}")
        
        error_msg = str(e).lower()
        
        if "401" in error_msg or "unauthorized" in error_msg:
            print_info("Possible causes:")
            print_info("  - Wrong email or password")
            print_info("  - LinkedIn account locked")
            print_info("  - 2FA enabled (not supported)")
        elif "challenge" in error_msg:
            print_info("LinkedIn is challenging your login")
            print_info("  - Try logging in via browser first")
            print_info("  - Complete any security challenges")
            print_info("  - Then try again")
        
        return None

def test_profile_fetch(api, profile_url):
    """Test fetching a LinkedIn profile."""
    print_header("Step 4: Testing Profile Fetch")
    
    if not api:
        print_error("Cannot test without authentication")
        return False
    
    # Extract username from URL
    try:
        if '/in/' in profile_url:
            username = profile_url.split('/in/')[-1].rstrip('/').split('?')[0]
        else:
            print_error(f"Invalid LinkedIn URL format: {profile_url}")
            return False
        
        print_info(f"Extracted username: {username}")
        print_info("Fetching profile data...")
        
        profile = api.get_profile(username)
        
        if profile:
            print_success("✓ Profile fetched successfully!")
            print_info(f"Name: {profile.get('firstName', '')} {profile.get('lastName', '')}")
            print_info(f"Headline: {profile.get('headline', 'N/A')}")
            print_info(f"Location: {profile.get('locationName', 'N/A')}")
            return True
        else:
            print_error("Profile fetch returned empty data")
            return False
            
    except Exception as e:
        print_error(f"Profile fetch failed: {e}")
        
        error_msg = str(e).lower()
        
        if "404" in error_msg:
            print_info("Profile not found - check the URL")
        elif "403" in error_msg:
            print_info("Access forbidden - profile may be private")
        elif "429" in error_msg:
            print_info("Rate limit exceeded - wait an hour")
        
        return False

def main():
    """Run all tests."""
    print_header("LinkedIn Authentication & Scraping Test")
    
    print("This script will test your LinkedIn scraping setup.")
    print("It will check:")
    print("  1. If linkedin-api is installed")
    print("  2. If credentials are in .env")
    print("  3. If authentication works")
    print("  4. If profile fetching works")
    
    # Test 1: Import
    if not test_linkedin_api_import():
        print("\n" + "="*60)
        print("❌ FAILED: Install linkedin-api first")
        print("Run: pip install linkedin-api")
        print("="*60)
        return
    
    # Test 2: Credentials
    email, password = test_credentials()
    
    if not email or not password:
        print("\n" + "="*60)
        print("❌ FAILED: Add credentials to .env")
        print("\nAdd these lines to your .env file:")
        print("LINKEDIN_EMAIL=your_email@example.com")
        print("LINKEDIN_PASSWORD=your_password")
        print("="*60)
        return
    
    # Test 3: Authentication
    api = test_authentication(email, password)
    
    if not api:
        print("\n" + "="*60)
        print("❌ FAILED: Authentication error")
        print("\nPossible solutions:")
        print("  1. Double-check your LinkedIn email and password")
        print("  2. Disable 2FA on your LinkedIn account")
        print("  3. Try logging in via browser first")
        print("  4. Use a different LinkedIn account")
        print("  5. OR use mock data in the app (check 'Use Mock Data')")
        print("="*60)
        return
    
    # Test 4: Profile Fetch
    print("\nWhich profile would you like to test?")
    print("1. Your own profile (enter your URL)")
    print("2. A public profile (e.g., Bill Gates)")
    
    choice = input("\nEnter choice (1 or 2) or press Enter for option 2: ").strip()
    
    if choice == "1":
        profile_url = input("Enter your LinkedIn profile URL: ").strip()
    else:
        profile_url = "https://www.linkedin.com/in/williamhgates/"
        print_info(f"Testing with: {profile_url}")
    
    success = test_profile_fetch(api, profile_url)
    
    # Final summary
    print_header("Test Summary")
    
    if success:
        print_success("✓ All tests passed!")
        print("\nYour setup is working correctly.")
        print("You can now use real LinkedIn profiles in the app.")
        print("\nTo use in the app:")
        print("  1. Uncheck 'Use Mock Data'")
        print("  2. Enter your LinkedIn URL")
        print("  3. Leave email/password empty (will use .env)")
        print("  4. Click 'Process Profile'")
    else:
        print_error("Some tests failed")
        print("\nRecommendation: Use mock data for now")
        print("  1. Check 'Use Mock Data' in the app")
        print("  2. Click 'Process Profile'")
        print("  3. This will work without LinkedIn credentials")
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()