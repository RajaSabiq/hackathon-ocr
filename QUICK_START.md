# Quick Start Guide

## Prerequisites Check

Before starting, verify you have:

```bash
# Check Python (need 3.10+)
python --version

# Check Node.js (need 16+)
node --version

# Check Tesseract OCR
tesseract --version
```

If any are missing, install them first (see README.md).

## Installation Steps

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Windows users:** If you get errors, also run:
```bash
pip install python-magic-bin
```

### 2. Test Backend Setup

```bash
python test_imports.py
```

You should see all green checkmarks ✓. If you see errors, check TROUBLESHOOTING.md.

### 3. Install Frontend Dependencies

```bash
cd ../frontend
npm install
```

## Running the Application

### Option 1: Automatic (Recommended)

**Windows:**
```bash
start.bat
```

**Linux/macOS:**
```bash
chmod +x start.sh
./start.sh
```

This will:
- Start the backend on http://localhost:8000
- Start the frontend on http://localhost:3000
- Open your browser automatically

### Option 2: Manual (Two Terminals)

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

Wait for: `Application startup complete`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

Wait for: `Compiled successfully!`

## First Test

1. Open http://localhost:3000 in your browser
2. You should see the OCR Document Digitizer interface
3. Drag and drop an image file (PNG, JPG, JPEG, WEBP, or PDF)
4. Wait for processing (usually 5-30 seconds)
5. View extracted text with confidence scores

## Quick Test with API

Test the backend directly:

```bash
# Check health
curl http://localhost:8000/api/health

# Upload a file (replace with your file path)
curl -X POST http://localhost:8000/api/ocr/upload \
  -F "files=@path/to/your/image.jpg"
```

## Common First-Time Issues

### Backend won't start

**Error: "Tesseract not found"**
- Install Tesseract OCR
- Add to system PATH
- Restart terminal

**Error: "Module not found"**
- Run: `pip install -r requirements.txt`
- Make sure you're in the `backend` directory

### Frontend won't start

**Error: "Port 3000 already in use"**
- Kill existing process or use different port
- Windows: `netstat -ano | findstr :3000` then `taskkill /PID <PID> /F`
- Linux/Mac: `lsof -ti:3000 | xargs kill -9`

**Error: "Module not found"**
- Run: `npm install`
- Delete `node_modules` and `package-lock.json`, then `npm install` again

### Upload fails

**Check these:**
1. Is backend running? Visit http://localhost:8000/api/health
2. Is file format supported? (PNG, JPG, JPEG, WEBP, PDF only)
3. Is file size under 10MB?
4. Check backend console for error messages

## Next Steps

- Read API_EXAMPLES.md for API usage
- Check TROUBLESHOOTING.md if you have issues
- Review PROJECT_STRUCTURE.md to understand the codebase
- Try different file types and formats

## Quick Commands Reference

```bash
# Start backend only
cd backend && python main.py

# Start frontend only
cd frontend && npm start

# Test backend imports
cd backend && python test_imports.py

# Run API tests
python test_api.py

# Check backend health
curl http://localhost:8000/api/health

# View supported formats
curl http://localhost:8000/api/supported-formats
```

## Getting Help

If something doesn't work:

1. Check the console output for error messages
2. Review TROUBLESHOOTING.md
3. Run `backend/test_imports.py` to verify setup
4. Check that Tesseract is installed: `tesseract --version`
5. Verify all dependencies: `pip list` and `npm list`

## Success Indicators

You'll know everything is working when:

- ✅ Backend shows: "Application startup complete"
- ✅ Frontend shows: "Compiled successfully!"
- ✅ Browser opens to http://localhost:3000
- ✅ Health check returns: `{"status":"healthy",...}`
- ✅ You can upload and process a test image

Happy OCR processing! 🎉