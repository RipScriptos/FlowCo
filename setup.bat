@echo off
REM FlowCo Setup Script for Windows
REM This script helps you set up the FlowCo AI Business Evaluation System

echo =========================================
echo FlowCo AI Business Evaluation System
echo Setup Script for Windows
echo =========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Create virtual environment
echo.
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Skipping...
) else (
    python -m venv venv
    echo Virtual environment created
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt

REM Create necessary directories
echo.
echo Creating necessary directories...
if not exist data mkdir data
if not exist temp mkdir temp
if not exist reports mkdir reports
if not exist templates mkdir templates
if not exist flowco\web\static\css mkdir flowco\web\static\css
if not exist flowco\web\static\js mkdir flowco\web\static\js
if not exist flowco\web\templates mkdir flowco\web\templates
echo Directories created

REM Check if .env file exists
echo.
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo .env file created
    echo.
    echo WARNING: Please edit .env file and add your API keys:
    echo    - OPENAI_API_KEY (for GPT models^)
    echo    - ANTHROPIC_API_KEY (for Claude models^)
    echo    Or set USE_LOCAL_MODELS=true to use Ollama
) else (
    echo .env file already exists
)

REM Check if config.yaml exists
echo.
if not exist config.yaml (
    echo Creating config.yaml from template...
    copy config.yaml.example config.yaml
    echo config.yaml created
) else (
    echo config.yaml already exists
)

echo.
echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo Next steps:
echo 1. Edit .env file and add your API keys
echo 2. Run the application:
echo    venv\Scripts\activate.bat
echo    python main.py
echo 3. Open your browser to http://localhost:12000
echo.
echo For more information, see README.md
echo.
pause