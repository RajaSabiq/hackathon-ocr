# OCR Application Troubleshooting Guide

## Quick Diagnostics

### 1. Test Backend Dependencies
```bash
cd backend
python test_imports.py
```

This will check if all required packages are installed and working.

### 2. Check Backend Logs
When you start the backend, watch for error messages in the console. Common issues:

- **Tesseract not found**: Install Tesseract OCR
- **Import errors**: Run `pip install -r requirements.txt`
- **Port already in use**: Change port in config or kill existing process

## Common Issues and Solutions

### Issue 1: Upload Fails with No Error Message

**Symptoms:**
- File upload returns error
- No detailed error message shown
- Backend logs show exceptions

**Solutions:**

1. **Check Tesseract Installation:**
   ```bash
   tesseract --version
   ```
   If not found, install:
   - Windows: `choco install tesseract` or download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - Ubuntu: `sudo apt-get install tesseract-ocr`
   - macOS: `brew install tesseract`

2. **Verify Python Dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Check File Permissions:**
   - Ensure `backend/uploads/` directory exists and is writable
   - On Linux/Mac: `chmod 755 backend/uploads`

4. **Review Backend Logs:**
   - Start backend and watch console output
   - Look for detailed error messages with stack traces

### Issue 2: "python-magic" Import Error

**Symptoms:**
- Backend fails to start
- Error: `ModuleNotFoundError: No module named 'magic'`

**Solutions:**

**Windows:**
```bash
pip install python-magic-bin
```

**Linux/macOS:**
```bash
pip install python-magic
# Also install system library:
# Ubuntu: sudo apt-get install libmagic1
# macOS: brew install libmagic
```

**Note:** The application now has fallback MIME detection, so this is optional.

### Issue 3: Tesseract OCR Errors

**Symptoms:**
- Upload succeeds but processing fails
- Error: "Tesseract is not installed"
- Error: "Failed to execute tesseract"

**Solutions:**

1. **Verify Tesseract is in PATH:**
   ```bash
   tesseract --version
   ```

2. **Windows - Add to PATH manually:**
   - Find Tesseract installation (usually `C:\Program Files\Tesseract-OCR`)
   - Add to System PATH environment variable
   - Restart terminal/IDE

3. **Set Tesseract Path Explicitly (if needed):**
   
   Create `backend/.env` file:
   ```
   TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
   ```
   
   Or in code, add to `backend/ocr_processor.py`:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

### Issue 4: PDF Processing Fails

**Symptoms:**
- Image files work but PDFs fail
- Error: "Unable to convert PDF"

**Solutions:**

1. **Install Poppler (required for pdf2image):**

   **Windows:**
   - Download from: https://github.com/oschwartz10612/poppler-windows/releases
   - Extract and add `bin` folder to PATH
   - Or use: `choco install poppler`

   **Ubuntu:**
   ```bash
   sudo apt-get install poppler-utils
   ```

   **macOS:**
   ```bash
   brew install poppler
   ```

2. **Verify Poppler Installation:**
   ```bash
   pdftoppm -v
   ```

### Issue 5: CORS Errors in Frontend

**Symptoms:**
- Frontend can't connect to backend
- Browser console shows CORS errors
- Network requests blocked

**Solutions:**

1. **Check Backend is Running:**
   - Backend should be on `http://localhost:8000`
   - Visit `http://localhost:8000/api/health` in browser

2. **Verify CORS Configuration:**
   - Check `backend/config.py` has correct origins
   - Default: `http://localhost:3000,http://127.0.0.1:3000`

3. **Use Correct Frontend URL:**
   - Frontend should be on `http://localhost:3000`
   - Don't use `127.0.0.1` if backend expects `localhost`

### Issue 6: Large Files Fail to Upload

**Symptoms:**
- Small files work, large files fail
- Upload times out
- Error: "Request Entity Too Large"

**Solutions:**

1. **Check File Size Limit:**
   - Default: 10MB per file
   - Increase in `backend/config.py`: `MAX_FILE_SIZE`

2. **Adjust Timeout:**
   - Frontend: Check `frontend/src/services/api.js` timeout setting
   - Default: 300000ms (5 minutes)

3. **Server Timeout:**
   - If using nginx/proxy, increase timeout settings

### Issue 7: Low OCR Accuracy

**Symptoms:**
- Text extracted but with many errors
- Low confidence scores
- Garbled output

**Solutions:**

1. **Image Quality:**
   - Use high-resolution images (300+ DPI)
   - Ensure good contrast
   - Avoid shadows and glare

2. **Image Preprocessing:**
   - The app automatically preprocesses images
   - For very poor quality, try manual enhancement first

3. **Language Detection:**
   - Ensure correct language is detected
   - Install additional Tesseract language packs if needed

4. **Tesseract Configuration:**
   - Adjust `TESSERACT_CONFIG` in `backend/config.py`
   - Try different PSM modes (1-13)

### Issue 8: Frontend Won't Start

**Symptoms:**
- `npm start` fails
- Port 3000 already in use
- Module not found errors

**Solutions:**

1. **Install Dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Clear Cache:**
   ```bash
   npm cache clean --force
   rm -rf node_modules package-lock.json
   npm install
   ```

3. **Port Already in Use:**
   ```bash
   # Kill process on port 3000
   # Windows:
   netstat -ano | findstr :3000
   taskkill /PID <PID> /F
   
   # Linux/Mac:
   lsof -ti:3000 | xargs kill -9
   ```

4. **Node Version:**
   - Ensure Node.js 16+ is installed
   - Check: `node --version`

## Debugging Tips

### Enable Debug Mode

1. **Backend Debug Logging:**
   
   Set environment variable:
   ```bash
   # Windows
   set DEBUG=true
   
   # Linux/Mac
   export DEBUG=true
   ```
   
   Or create `backend/.env`:
   ```
   DEBUG=true
   LOG_LEVEL=DEBUG
   ```

2. **Check Backend Health:**
   ```bash
   curl http://localhost:8000/api/health
   ```

3. **Test Upload Manually:**
   ```bash
   curl -X POST http://localhost:8000/api/ocr/upload \
     -F "files=@test_image.jpg"
   ```

### View Detailed Logs

**Backend:**
- All logs print to console
- Look for ERROR and WARNING messages
- Stack traces show exact error location

**Frontend:**
- Open browser DevTools (F12)
- Check Console tab for errors
- Check Network tab for failed requests

### Test Individual Components

1. **Test Tesseract Directly:**
   ```bash
   tesseract test_image.jpg output
   cat output.txt
   ```

2. **Test Image Preprocessing:**
   ```python
   from backend.image_preprocessor import ImagePreprocessor
   preprocessor = ImagePreprocessor()
   result = preprocessor.preprocess_image("test.jpg")
   ```

3. **Test OCR Processor:**
   ```python
   from backend.ocr_processor import OCRProcessor
   processor = OCRProcessor()
   results = processor.process_file("test.jpg", "test.jpg")
   print(results[0].text)
   ```

## Getting Help

If you're still experiencing issues:

1. **Check Logs:**
   - Backend console output
   - Browser console (F12)
   - Network tab in DevTools

2. **Verify Setup:**
   - Run `backend/test_imports.py`
   - Check all dependencies installed
   - Verify Tesseract and Poppler in PATH

3. **Test with Sample Files:**
   - Try with simple, clean images first
   - Use provided sample images
   - Test one file at a time

4. **Common Error Messages:**

   | Error | Likely Cause | Solution |
   |-------|-------------|----------|
   | "Tesseract not found" | Tesseract not installed/in PATH | Install Tesseract, add to PATH |
   | "Could not load image" | Invalid file format | Check file is valid image/PDF |
   | "MIME type error" | File validation failed | Ensure file extension matches content |
   | "Connection refused" | Backend not running | Start backend server |
   | "CORS error" | Frontend/backend mismatch | Check CORS config, use correct URLs |
   | "Timeout" | File too large/slow processing | Reduce file size, increase timeout |

## Performance Optimization

### Slow Processing

1. **Reduce Image Size:**
   - Adjust `MAX_IMAGE_DIMENSION` in config
   - Smaller images process faster

2. **Disable Preprocessing Steps:**
   - Comment out slow steps in `image_preprocessor.py`
   - Trade accuracy for speed

3. **Use Faster Tesseract Mode:**
   - Change `--oem 3` to `--oem 1` in config
   - Legacy engine is faster but less accurate

### Memory Issues

1. **Reduce Batch Size:**
   - Lower `MAX_BATCH_SIZE` in config
   - Process fewer files at once

2. **Clear Job Storage:**
   - Reduce `MAX_JOBS_IN_MEMORY`
   - Implement periodic cleanup

## System Requirements

**Minimum:**
- Python 3.10+
- Node.js 16+
- 4GB RAM
- Tesseract OCR 4.0+

**Recommended:**
- Python 3.11+
- Node.js 18+
- 8GB RAM
- Tesseract OCR 5.0+
- SSD storage

## Still Having Issues?

Create a detailed bug report with:
- Operating system and version
- Python version (`python --version`)
- Node version (`node --version`)
- Tesseract version (`tesseract --version`)
- Complete error message and stack trace
- Steps to reproduce
- Sample file that causes the issue (if applicable)