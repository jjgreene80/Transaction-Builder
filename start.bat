@echo off
echo ============================================================
echo  TC Doc Tool - Transaction File Organizer
echo ============================================================
echo.

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Install Python 3.10+ from python.org
    pause
    exit /b 1
)

:: Check Node
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js not found. Install from nodejs.org
    pause
    exit /b 1
)

echo [1/4] Installing Python dependencies...
cd /d "%~dp0backend"
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install Python packages.
    pause
    exit /b 1
)

echo [2/4] Installing frontend dependencies...
cd /d "%~dp0frontend"
call npm install --silent
if errorlevel 1 (
    echo ERROR: Failed to install npm packages.
    pause
    exit /b 1
)

echo [3/4] Starting backend (port 8000)...
cd /d "%~dp0backend"
start "TC Doc Tool - Backend" cmd /k "python -m uvicorn main:app --reload --port 8000"

echo [4/4] Starting frontend (port 5173)...
cd /d "%~dp0frontend"
timeout /t 2 /nobreak >nul
start "TC Doc Tool - Frontend" cmd /k "npm run dev"

echo.
echo ============================================================
echo  App running at: http://localhost:5173
echo  API running at: http://localhost:8000
echo.
echo  NOTE: For OCR on scanned PDFs, install Tesseract:
echo  https://github.com/UB-Mannheim/tesseract/wiki
echo  Then add it to your PATH.
echo ============================================================
echo.
timeout /t 3 /nobreak >nul
start http://localhost:5173
