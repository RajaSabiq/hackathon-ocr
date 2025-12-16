# OCR API Examples

This document provides practical examples of how to use the OCR Document Digitizer API.

## Base URL
```
http://localhost:8000
```

## Authentication
No authentication required for local development.

## API Endpoints

### 1. Health Check

Check if the API is running and get system information.

**Request:**
```bash
curl -X GET "http://localhost:8000/api/health"
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "tesseract_version": "5.3.0"
}
```

### 2. Get Supported Formats

Get information about supported file formats and limits.

**Request:**
```bash
curl -X GET "http://localhost:8000/api/supported-formats"
```

**Response:**
```json
{
  "supported_extensions": [".png", ".jpg", ".jpeg", ".webp", ".pdf"],
  "supported_mime_types": ["image/png", "image/jpeg", "image/jpg", "image/webp", "application/pdf"],
  "max_file_size_mb": 10,
  "max_batch_size": 10
}
```

### 3. Upload Documents for OCR

Upload one or more documents for OCR processing.

**Single File Upload:**
```bash
curl -X POST "http://localhost:8000/api/ocr/upload" \
  -F "files=@document.jpg"
```

**Multiple Files Upload:**
```bash
curl -X POST "http://localhost:8000/api/ocr/upload" \
  -F "files=@document1.jpg" \
  -F "files=@document2.pdf" \
  -F "files=@document3.png"
```

**Response:**
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "processing",
  "files_count": 3
}
```

### 4. Get OCR Results

Retrieve the results of an OCR job using the job ID.

**Request:**
```bash
curl -X GET "http://localhost:8000/api/ocr/result/123e4567-e89b-12d3-a456-426614174000"
```

**Response (Processing):**
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "processing",
  "results": [],
  "error_message": null
}
```

**Response (Completed):**
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "completed",
  "results": [
    {
      "filename": "document1.jpg",
      "text": "This is the extracted text from the document...",
      "confidence": 0.92,
      "language": "eng",
      "bbox_data": [
        {
          "text": "This",
          "confidence": 0.95,
          "bbox": [10, 20, 30, 15]
        },
        {
          "text": "is",
          "confidence": 0.89,
          "bbox": [45, 20, 15, 15]
        }
      ],
      "page_number": null
    },
    {
      "filename": "document2.pdf (Page 1)",
      "text": "PDF content from page 1...",
      "confidence": 0.88,
      "language": "eng",
      "bbox_data": [...],
      "page_number": 1
    }
  ],
  "error_message": null
}
```

**Response (Failed):**
```json
{
  "job_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "failed",
  "results": [],
  "error_message": "Error processing file: Unsupported format"
}
```

### 5. Delete Job

Clean up a completed job and its results.

**Request:**
```bash
curl -X DELETE "http://localhost:8000/api/ocr/job/123e4567-e89b-12d3-a456-426614174000"
```

**Response:**
```json
{
  "message": "Job deleted successfully"
}
```

## JavaScript Examples

### Using Fetch API

```javascript
// Upload files
async function uploadFiles(files) {
  const formData = new FormData();
  
  Array.from(files).forEach(file => {
    formData.append('files', file);
  });
  
  const response = await fetch('http://localhost:8000/api/ocr/upload', {
    method: 'POST',
    body: formData
  });
  
  return await response.json();
}

// Poll for results
async function pollForResults(jobId) {
  while (true) {
    const response = await fetch(`http://localhost:8000/api/ocr/result/${jobId}`);
    const result = await response.json();
    
    if (result.status === 'completed' || result.status === 'failed') {
      return result;
    }
    
    // Wait 2 seconds before next poll
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}

// Complete workflow
async function processDocuments(files) {
  try {
    // Upload files
    const uploadResult = await uploadFiles(files);
    console.log('Upload started:', uploadResult.job_id);
    
    // Poll for results
    const finalResult = await pollForResults(uploadResult.job_id);
    
    if (finalResult.status === 'completed') {
      console.log('OCR completed:', finalResult.results);
      return finalResult.results;
    } else {
      console.error('OCR failed:', finalResult.error_message);
      throw new Error(finalResult.error_message);
    }
  } catch (error) {
    console.error('Error:', error);
    throw error;
  }
}
```

### Using Axios

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 300000 // 5 minutes
});

// Upload and process files
async function processWithAxios(files) {
  const formData = new FormData();
  files.forEach(file => formData.append('files', file));
  
  // Upload
  const uploadResponse = await api.post('/api/ocr/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  
  const jobId = uploadResponse.data.job_id;
  
  // Poll for results
  while (true) {
    const resultResponse = await api.get(`/api/ocr/result/${jobId}`);
    const result = resultResponse.data;
    
    if (result.status !== 'processing') {
      return result;
    }
    
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
}
```

## Python Examples

### Using Requests

```python
import requests
import time
from pathlib import Path

API_BASE = "http://localhost:8000"

def upload_files(file_paths):
    """Upload files for OCR processing"""
    files = []
    for file_path in file_paths:
        files.append(('files', open(file_path, 'rb')))
    
    response = requests.post(f"{API_BASE}/api/ocr/upload", files=files)
    
    # Close file handles
    for _, file_handle in files:
        file_handle.close()
    
    return response.json()

def get_results(job_id):
    """Get OCR results for a job"""
    response = requests.get(f"{API_BASE}/api/ocr/result/{job_id}")
    return response.json()

def poll_for_results(job_id, max_attempts=60):
    """Poll for job completion"""
    for _ in range(max_attempts):
        result = get_results(job_id)
        
        if result['status'] in ['completed', 'failed']:
            return result
        
        time.sleep(2)
    
    raise TimeoutError("Job processing timeout")

# Example usage
if __name__ == "__main__":
    # Upload files
    file_paths = ["document1.jpg", "document2.pdf"]
    upload_result = upload_files(file_paths)
    print(f"Job ID: {upload_result['job_id']}")
    
    # Get results
    final_result = poll_for_results(upload_result['job_id'])
    
    if final_result['status'] == 'completed':
        for result in final_result['results']:
            print(f"File: {result['filename']}")
            print(f"Confidence: {result['confidence']:.2%}")
            print(f"Text: {result['text'][:100]}...")
            print("-" * 50)
    else:
        print(f"Error: {final_result['error_message']}")
```

## Error Handling

### Common HTTP Status Codes

- **200**: Success
- **400**: Bad Request (invalid files, too many files, etc.)
- **404**: Job not found
- **413**: File too large
- **422**: Validation error
- **500**: Internal server error
- **503**: Service unavailable

### Error Response Format

```json
{
  "detail": "Error description here"
}
```

### Best Practices

1. **Always check file size** before uploading (max 10MB per file)
2. **Validate file formats** (PNG, JPG, JPEG, WEBP, PDF only)
3. **Implement proper polling** with reasonable intervals (2-5 seconds)
4. **Handle timeouts** gracefully (OCR can take time for large files)
5. **Clean up jobs** after processing to free memory
6. **Implement retry logic** for network failures

## Rate Limiting

Currently no rate limiting is implemented, but consider:
- Maximum 10 files per batch
- Reasonable polling intervals
- Clean up completed jobs

## WebSocket Alternative (Future Enhancement)

For real-time updates, consider implementing WebSocket connections:

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/ocr/{job_id}');

ws.onmessage = function(event) {
  const update = JSON.parse(event.data);
  console.log('Status update:', update);
};
```