@echo off
REM ============================================================================
REM LinkedIn Icebreaker Bot - Quick Setup for Windows
REM ============================================================================

color 0A
title LinkedIn Icebreaker - Gemini Migration

echo.
echo ========================================
echo LinkedIn Icebreaker Bot
echo Gemini Migration - Quick Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9+ from python.org
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version

echo.
echo ========================================
echo Step 1: Activating Virtual Environment
echo ========================================
echo.

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
) else (
    echo [INFO] Virtual environment not found, creating...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment created and activated
)

echo.
echo ========================================
echo Step 2: Backing Up Original Files
echo ========================================
echo.

if exist "config.py" (
    copy /Y config.py config.py.backup >nul
    echo [OK] Backed up config.py
)

if exist "modules\llm_interface.py" (
    copy /Y modules\llm_interface.py modules\llm_interface.py.backup >nul
    echo [OK] Backed up llm_interface.py
)

if exist "modules\data_processing.py" (
    copy /Y modules\data_processing.py modules\data_processing.py.backup >nul
    echo [OK] Backed up data_processing.py
)

if exist "modules\query_engine.py" (
    copy /Y modules\query_engine.py modules\query_engine.py.backup >nul
    echo [OK] Backed up query_engine.py
)

if exist "modules\data_extraction.py" (
    copy /Y modules\data_extraction.py modules\data_extraction.py.backup >nul
    echo [OK] Backed up data_extraction.py
)

echo.
echo ========================================
echo Step 3: Removing Old IBM Packages
echo ========================================
echo.

pip uninstall -y llama-index-llms-ibm llama-index-embeddings-ibm 2>nul
echo [OK] Old IBM packages removed

echo.
echo ========================================
echo Step 4: Installing Gemini Packages
echo ========================================
echo.

echo [INFO] Upgrading pip...
python -m pip install --upgrade pip --quiet

echo [INFO] Installing google-genai...
pip install google-genai --quiet

echo [INFO] Installing LlamaIndex Gemini integrations...
pip install llama-index-llms-google-genai llama-index-embeddings-google-genai --quiet

echo [INFO] Installing python-dotenv...
pip install python-dotenv --quiet

echo [OK] All Gemini packages installed

echo.
echo ========================================
echo Step 5: Checking .env File
echo ========================================
echo.

if not exist ".env" (
    echo [INFO] Creating .env file...
    (
        echo # Google Gemini API Key
        echo # Get from: https://aistudio.google.com/app/apikey
        echo GEMINI_API_KEY=your_gemini_api_key_here
        echo.
        echo # ProxyCurl API Key ^(optional^)
        echo PROXYCURL_API_KEY=
    ) > .env
    echo [OK] Created .env file
    echo.
    echo [IMPORTANT] Please edit .env and add your GEMINI_API_KEY
    echo Get it from: https://aistudio.google.com/app/apikey
) else (
    findstr /C:"GEMINI_API_KEY" .env >nul
    if errorlevel 1 (
        echo [INFO] Adding GEMINI_API_KEY to existing .env...
        echo. >> .env
        echo # Google Gemini API Key >> .env
        echo GEMINI_API_KEY=your_gemini_api_key_here >> .env
        echo [OK] Added GEMINI_API_KEY to .env
    ) else (
        echo [OK] .env file exists with GEMINI_API_KEY
    )
)

echo.
echo ========================================
echo Step 6: Package Verification
echo ========================================
echo.

echo [INFO] Installed Gemini packages:
pip list | findstr /C:"google-genai" /C:"llama-index-llms-google" /C:"llama-index-embeddings-google"

echo.
echo [INFO] Core packages preserved:
pip list | findstr /C:"llama-index-core" /C:"gradio"

echo.
echo ========================================
echo IMPORTANT: Manual File Updates Required
echo ========================================
echo.
echo You must now replace these files with the updated versions:
echo.
echo 1. config.py
echo    ^> Copy from artifact: "config.py (Updated for Gemini)"
echo.
echo 2. modules\llm_interface.py
echo    ^> Copy from artifact: "llm_interface.py (Updated for Gemini)"
echo.
echo 3. modules\data_processing.py
echo    ^> Copy from artifact: "data_processing.py (Updated for Gemini)"
echo.
echo 4. modules\query_engine.py
echo    ^> Copy from artifact: "query_engine.py (Updated for Gemini)"
echo.
echo 5. modules\data_extraction.py
echo    ^> Copy from artifact: "data_extraction.py (Updated for Gemini)"
echo.
echo 6. Edit .env file
echo    ^> Add your actual GEMINI_API_KEY
echo.

echo.
echo ========================================
echo Next Steps (After File Updates)
echo ========================================
echo.
echo 1. Replace the 5 files listed above with content from artifacts
echo 2. Edit .env and add your GEMINI_API_KEY
echo 3. Run: python test_gemini.py
echo 4. Run: python app.py
echo.
echo Backups saved as *.backup files
echo.
echo ========================================

pause

echo.
echo [INFO] Opening default text editor for .env file...
notepad .env

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Don't forget to:
echo 1. Replace the 5 Python files from artifacts
echo 2. Add your GEMINI_API_KEY to .env
echo 3. Test with: python test_gemini.py
echo.
pause