@echo off
REM ==============================================================================
REM HarnessEval — One-click setup & launch (Windows)
REM
REM Usage: Double-click or run in Command Prompt:
REM   start_harness_eval.bat
REM ==============================================================================

cd /d "%~dp0"

echo ========================================
echo   HarnessEval - Setup ^& Launch
echo   Modular Harness Evaluation Toolkit
echo ========================================
echo.

REM --- Step 1: Check Python ---
echo [1/7] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.10+ first.
    pause
    exit /b 1
)
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PY_VER=%%v
echo   Python %PY_VER% OK

REM --- Step 2: Virtual environment ---
echo [2/7] Setting up virtual environment...
if not exist ".venv" (
    echo   Creating .venv...
    python -m venv .venv
)
call .venv\Scripts\activate.bat
echo   .venv activated OK

REM --- Step 3: Install dependencies ---
echo [3/7] Installing dependencies...
pip install -e ".[dev]" -q 2>nul
echo   Dependencies installed OK

REM --- Step 4: Check .env ---
echo [4/7] Checking API keys...
if not exist ".env" (
    echo   Creating .env from .env.example...
    copy .env.example .env >nul
    echo   .env created - please add your API keys!
)

set HAS_KEY=0
for /f "tokens=1,2 delims==" %%a in (.env) do (
    if "%%b" neq "" (
        if "%%a"=="DEEPSEEK_API_KEY" (
            echo   DeepSeek: set
            set HAS_KEY=1
        )
        if "%%a"=="OPENAI_API_KEY" (
            echo   OpenAI: set
            set HAS_KEY=1
        )
        if "%%a"=="ANTHROPIC_API_KEY" (
            echo   Anthropic: set
            set HAS_KEY=1
        )
    )
)

if %HAS_KEY%==0 (
    echo.
    echo   No API keys found in .env
    echo   You can still use Ollama mode (free) or Dry-run mode.
    echo   To add keys: edit .env file
    echo.
)

REM --- Step 5: Check Ollama ---
echo [5/7] Checking Ollama...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo   Ollama not installed (optional)
    echo   Install: https://ollama.com/download
) else (
    echo   Ollama installed OK
)

REM --- Step 6: Directories ---
echo [6/7] Preparing directories...
if not exist "trajectories" mkdir trajectories
echo   trajectories/ ready OK

REM --- Step 7: Launch ---
echo.
echo ========================================
echo   Launching HarnessEval Dashboard
echo   http://localhost:8501
echo ========================================
echo.

streamlit run streamlit_app.py --server.port 8501
