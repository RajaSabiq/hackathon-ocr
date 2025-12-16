# How to Test the OCR Fix

## Quick Test (Recommended)

### 1. Verify the Fix
```bash
python test_ocr_fix.py
```

Expected output:
```
🎉 All tests passed!
✓ OCR configuration is compatible with your Tesseract version
✓ You can now restart the backend and test with real images
```

### 2. Restart Backend
```bash
cd backend
python main.py
```

Look for these log messages:
```
Tesseract version detected: 3.02
Tesseract 3.x detected. For better accuracy, consider upgrading to Tesseract 5.x
```

### 3. Test with Real Image

**Option A: Use the test script**
```bash
python test_api.py
```

**Option B: Use the web interface**
1. Start frontend: `cd frontend && npm start`
2. Open http://localhost:3000
3. Upload an image
4. Verify text is extracted

**Option C: Use curl**
```bash
# Upload
curl -X POST http://localhost:8000/api/ocr/upload \
  -F "files=@your-image.png"

# Get result (use job_id from upload response)
curl http://localhost:8000/api/ocr/result/{job_id}
```

## What to Look For

### ✅ Success Indicators:
- Upload returns job_id
- Status changes from "processing" to "completed"
- Results contain extracted text
- Confidence scores are present
- No error messages in logs

### ❌ Failure Indicators:
- Status stays "processing" forever
- Status changes to "failed"
- Empty text in results
- Error messages in backend logs

## Troubleshooting

### If OCR still doesn't work:

1. **Check Tesseract is installed:**
   ```bash
   tesseract --version
   ```

2. **Check backend logs:**
   Look for error messages in the terminal running `python main.py`

3. **Verify file format:**
   - Supported: PNG, JPG, JPEG, WEBP, PDF
   - Max size: 10MB

4. **Try a simple test image:**
   Create a simple image with clear text (black text on white background)

5. **Check Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

## Expected Results

### Sample API Response (Success):
```json
{
  "job_id": "abc-123-def-456",
  "status": "completed",
  "results": [
    {
      "filename": "test.png",
      "text": "Extracted text from your image...",
      "confidence": 0.92,
      "language": "eng",
      "bbox_data": [
        {
          "text": "Extracted",
          "confidence": 0.95,
          "bbox": [10, 20, 100, 30]
        }
      ],
      "page_number": null
    }
  ],
  "error_message": null
}
```

## Performance Notes

With Tesseract 3.02:
- ✅ OCR works correctly
- ⚠️  Accuracy may be lower than Tesseract 5.x
- ⚠️  Processing may be slower
- ⚠️  Some advanced features may not work

For best results, consider upgrading to Tesseract 5.x (see ISSUE_DIAGNOSIS.md for instructions).
