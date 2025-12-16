#!/bin/bash

echo "========================================"
echo "OCR Document Digitizer - Startup Script"
echo "========================================"
echo

# Check Python installation
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.10+ from https://python.org"
    exit 1
fi

# Check Node.js installation
echo "Checking Node.js installation..."
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js 16+ from https://nodejs.org"
    exit 1
fi

# Check Tesseract installation
echo "Checking Tesseract installation..."
if ! command -v tesseract &> /dev/null; then
    echo "ERROR: Tesseract OCR is not installed"
    echo "Please install Tesseract:"
    echo "  Ubuntu/Debian: sudo apt-get install tesseract-ocr"
    echo "  macOS: brew install tesseract"
    echo "  Or visit: https://github.com/tesseract-ocr/tesseract"
    exit 1
fi

echo
echo "All dependencies found!"
echo

# Install Python dependencies
echo "Installing Python dependencies..."
cd backend
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Python dependencies"
    exit 1
fi

# Install Node.js dependencies
echo
echo "Installing Node.js dependencies..."
cd ../frontend
npm install
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install Node.js dependencies"
    exit 1
fi

echo
echo "========================================"
echo "Starting OCR Application..."
echo "========================================"
echo
echo "Backend will start on: http://localhost:8000"
echo "Frontend will start on: http://localhost:3000"
echo
echo "Press Ctrl+C to stop the application"
echo

# Start backend in background
echo "Starting backend server..."
cd ../backend
python3 main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "Starting frontend server..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo
echo "Both servers are running..."
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo
echo "The application will open in your browser automatically."
echo "Press Ctrl+C to stop both servers."

# Wait for user interrupt
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait