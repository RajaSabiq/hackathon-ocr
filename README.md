# OCR Document Digitizer

A production-ready OCR web application that digitizes customer documents (IDs, invoices, forms) with high accuracy, clean UI, and well-structured APIs.

## Features

- **Multi-format Support**: PNG, JPG, JPEG, WEBP, PDF (single & multi-page)
- **Drag & Drop Upload**: Intuitive file upload with preview
- **Batch Processing**: Upload multiple images simultaneously
- **High Accuracy OCR**: Advanced preprocessing and Tesseract OCR engine
- **Confidence Scoring**: Per-word confidence levels with visual indicators
- **Text Export**: Copy to clipboard or download as TXT
- **Multi-language Support**: Automatic language detection
- **Bounding Box Visualization**: Visual overlay of detected text regions

## Tech Stack

### Backend
- **FastAPI**: High-performance REST API
- **Tesseract OCR**: Industry-standard OCR engine
- **OpenCV**: Advanced image preprocessing
- **Pillow**: Image manipulation
- **pdf2image**: PDF processing

### Frontend
- **React**: Modern UI framework
- **Drag & Drop**: Native file upload
- **Responsive Design**: Clean, professional interface

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 16+
- Tesseract OCR

### Installation

1. **Install Tesseract OCR**:
   ```bash
   # Windows (using chocolatey)
   choco install tesseract
   
   # Windows (manual): Download from https://github.com/UB-Mannheim/tesseract/wiki
   # Ubuntu/Debian: sudo apt-get install tesseract-ocr
   # macOS: brew install tesseract
   ```

2. **Clone and Setup Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Setup Frontend**:
   ```bash
   cd frontend
   npm install
   ```

### Running the Application

#### Option 1: Automatic Startup (Recommended)

**Windows:**
```bash
start.bat
```

**Linux/macOS:**
```bash
./start.sh
```

#### Option 2: Manual Startup

1. **Start Backend** (Terminal 1):
   ```bash
   cd backend
   python main.py
   ```
   Backend runs on: http://localhost:8000

2. **Start Frontend** (Terminal 2):
   ```bash
   cd frontend
   npm start
   ```
   Frontend runs on: http://localhost:3000

#### Option 3: Test the API

After starting the backend, test it with:
```bash
python test_api.py
```

## API Documentation

### Upload Document
```http
POST /api/ocr/upload
Content-Type: multipart/form-data

files: File[] (PNG, JPG, JPEG, WEBP, PDF)
```

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "processing",
  "files_count": 2
}
```

### Get OCR Results
```http
GET /api/ocr/result/{job_id}
```

**Response:**
```json
{
  "job_id": "uuid-string",
  "status": "completed",
  "results": [
    {
      "filename": "document.jpg",
      "text": "Extracted text content...",
      "confidence": 0.92,
      "language": "eng",
      "bbox_data": [
        {
          "text": "word",
          "confidence": 0.95,
          "bbox": [x, y, width, height]
        }
      ]
    }
  ]
}
```

## Supported Formats

- **Images**: PNG, JPG, JPEG, WEBP
- **Documents**: PDF (single & multi-page)
- **Languages**: Auto-detection (100+ languages supported)

## Testing Scenarios

The application handles:
- ✅ Clean printed documents
- ✅ Handwritten text
- ✅ Receipts & invoices
- ✅ Business cards
- ✅ Skewed/rotated images
- ✅ Low quality/blurry images
- ✅ Multi-language documents
- ✅ PDF documents (single & multi-page)

## Project Structure

```
ocr-app/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── ocr_processor.py     # OCR processing logic
│   ├── image_preprocessor.py # Image preprocessing
│   ├── models.py           # Pydantic models
│   ├── requirements.txt    # Python dependencies
│   └── uploads/           # Temporary file storage
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/     # API services
│   │   └── App.js       # Main application
│   ├── package.json     # Node dependencies
│   └── public/         # Static assets
└── README.md
```

## Error Handling

The application includes comprehensive error handling for:
- Invalid file formats
- Corrupt images
- Unsupported formats
- Network timeouts
- OCR processing failures

## Production Considerations

- File size limits (10MB per file)
- Temporary file cleanup
- Rate limiting ready
- CORS configuration
- Error logging
- Health check endpoints