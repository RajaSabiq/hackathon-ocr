@echo off
echo ========================================
echo OCR Document Digitizer - Startup Script
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

echo Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from https://nodejs.org
    pause
    exit /b 1
)

echo Checking Tesseract installation...
tesseract --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Tesseract OCR is not installed or not in PATH
    echo Please install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
    echo Or use chocolatey: choco install tesseract
    pause
    exit /b 1
)

echo.
echo All dependencies found!
echo.

echo Installing Python dependencies...
cd backend
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

echo.
echo Installing Node.js dependencies...
cd ..\frontend
call npm install
if errorlevel 1 (
    echo ERROR: Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Starting OCR Application...
echo ========================================
echo.
echo Backend will start on: http://localhost:8000
echo Frontend will start on: http://localhost:3000
echo.
echo Press Ctrl+C in either window to stop the application
echo.

echo Starting backend server...
start "OCR Backend" cmd /k "cd ..\backend && python main.py"

timeout /t 3 /nobreak >nul

echo Starting frontend server...
start "OCR Frontend" cmd /k "npm start"

echo.
echo Both servers are starting...
echo The application will open in your browser automatically.
echo.
pause