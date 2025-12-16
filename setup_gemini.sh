#!/bin/bash

# ============================================================================
# Setup Script for Migrating to Google Gemini
# ============================================================================

echo "=========================================="
echo "LinkedIn Icebreaker Bot - Gemini Migration"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check if Python 3.9+
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 9) else 1)"; then
    echo -e "${GREEN}✓ Python 3.9+ detected${NC}"
else
    echo -e "${RED}✗ Python 3.9+ required. Please upgrade your Python.${NC}"
    exit 1
fi

echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${YELLOW}ℹ Virtual environment already exists${NC}"
fi

echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

echo ""

# Uninstall old IBM watsonx packages
echo "Removing old IBM watsonx packages..."
pip uninstall -y ibm-watsonx-ai ibm-watson-machine-learning 2>/dev/null
echo -e "${GREEN}✓ Old packages removed${NC}"

echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo -e "${GREEN}✓ pip upgraded${NC}"

echo ""

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi

echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit .env file and add your GEMINI_API_KEY${NC}"
    echo "  Get a free API key from: https://aistudio.google.com/app/apikey"
else
    echo -e "${YELLOW}ℹ .env file already exists${NC}"
fi

echo ""

# Check if GEMINI_API_KEY is set
if grep -q "your_gemini_api_key_here" .env 2>/dev/null; then
    echo -e "${YELLOW}⚠ GEMINI_API_KEY not set in .env file${NC}"
    echo "  Please edit .env and add your API key"
else
    echo -e "${GREEN}✓ GEMINI_API_KEY appears to be set${NC}"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Make sure GEMINI_API_KEY is set in .env file"
echo "2. Test the installation:"
echo "   python test_gemini.py"
echo "3. Run the application:"
echo "   python app.py"
echo ""
echo "For testing with mock data:"
echo "   python main.py --mock"
echo ""