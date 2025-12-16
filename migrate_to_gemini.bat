@echo off
REM ============================================================================
REM LinkedIn Icebreaker Bot - Gemini Migration Script (Windows)
REM Tailored for your specific setup with llama-index-core==0.11.8
REM ============================================================================

echo ==========================================
echo LinkedIn Icebreaker Bot
echo IBM watsonx -^> Google Gemini Migration
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [*] Creating virtual environment...
    python -m venv venv
    echo [+] Virtual environment created
) else (
    echo [+] Virtual environment already exists
)

echo.
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo ==========================================
echo Step 1: Backing up current setup
echo ==========================================
echo.

if exist "requirements.txt" (
    copy requirements.txt requirements.txt.backup >nul
    echo [+] Backed up requirements.txt
)

if exist "config.py" (
    copy config.py config.py.backup >nul
    echo [+] Backed up config.py
)

if exist "modules\llm_interface.py" (
    copy modules\llm_interface.py modules\llm_interface.py.backup >nul
    echo [+] Backed up llm_interface.py
)

echo.
echo ==========================================
echo Step 2: Removing IBM watsonx packages
echo ==========================================
echo.

pip uninstall -y llama-index-llms-ibm llama-index-embeddings-ibm 2>nul
echo [+] IBM packages removed

echo.
echo ==========================================
echo Step 3: Upgrading pip
echo ==========================================
echo.

python -m pip install --upgrade pip
echo [+] pip upgraded

echo.
echo ==========================================
echo Step 4: Installing Google Gemini packages
echo ==========================================
echo.

echo [*] Installing google-genai...
pip install google-genai

echo [*] Installing llama-index Gemini integrations...
pip install llama-index-llms-google-genai llama-index-embeddings-google-genai

echo [*] Installing python-dotenv...
pip install python-dotenv

echo [+] Gemini packages installed

echo.
echo ==========================================
echo Step 5: Verifying existing packages
echo ==========================================
echo.

pip list | findstr /C:"llama-index-core" /C:"gradio" /C:"requests" /C:"pydantic"
echo [+] Existing packages verified

echo.
echo ==========================================
echo Step 6: Setting up environment variables
echo ==========================================
echo.

if not exist ".env" (
    echo # ============================================================================ > .env
    echo # Google Gemini API Configuration >> .env
    echo # ============================================================================ >> .env
    echo # Get your free API key from: https://aistudio.google.com/app/apikey >> .env
    echo GEMINI_API_KEY=your_gemini_api_key_here >> .env
    echo. >> .env
    echo # ============================================================================ >> .env
    echo # ProxyCurl API Configuration >> .env
    echo # ============================================================================ >> .env
    echo # Get your API key from: https://nubela.co/proxycurl >> .env
    echo # Note: You can use mock data for testing without this key >> .env
    echo PROXYCURL_API_KEY=your_proxycurl_api_key_here >> .env
    
    echo [+] Created .env file
    echo [!] Please edit .env and add your GEMINI_API_KEY
) else (
    echo [!] .env file already exists
    findstr /C:"GEMINI_API_KEY" .env >nul
    if errorlevel 1 (
        echo. >> .env
        echo # Google Gemini API Key >> .env
        echo GEMINI_API_KEY=your_gemini_api_key_here >> .env
        echo [!] Added GEMINI_API_KEY to .env
    )
)

echo.
echo ==========================================
echo Migration Summary
echo ==========================================
echo.
echo [+] Installed Packages:
pip list | findstr /C:"google-genai" /C:"llama-index-llms-google" /C:"llama-index-embeddings-google"
echo.
echo [+] Preserved Packages:
pip list | findstr /C:"llama-index-core" /C:"gradio" /C:"huggingface-hub"
echo.
echo [-] Removed Packages:
echo   - llama-index-llms-ibm
echo   - llama-index-embeddings-ibm

echo.
echo ==========================================
echo Next Steps
echo ==========================================
echo.
echo 1. Update config.py
echo    Copy the new config.py from the artifacts provided
echo.
echo 2. Update modules\llm_interface.py
echo    Copy the new llm_interface.py from the artifacts provided
echo.
echo 3. Add your Gemini API Key
echo    Edit .env and add: GEMINI_API_KEY=your_actual_key
echo    Get key from: https://aistudio.google.com/app/apikey
echo.
echo 4. Test the migration
echo    Run: python test_gemini.py
echo.
echo 5. Run the application
echo    Run: python app.py
echo.
echo [+] Backups created:
echo   - requirements.txt.backup
echo   - config.py.backup
echo   - modules\llm_interface.py.backup
echo.
echo ==========================================
echo Migration script completed!
echo ==========================================
echo.
pause