# OCR Document Digitizer - Project Structure

```
ocr-app/
├── README.md                    # Main documentation
├── API_EXAMPLES.md             # API usage examples
├── PROJECT_STRUCTURE.md        # This file
├── .gitignore                  # Git ignore rules
├── start.bat                   # Windows startup script
├── start.sh                    # Unix/Linux startup script
├── test_api.py                 # API testing script
│
├── backend/                    # Python FastAPI backend
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Configuration settings
│   ├── models.py               # Pydantic data models
│   ├── ocr_processor.py        # OCR processing logic
│   ├── image_preprocessor.py   # Image preprocessing pipeline
│   ├── requirements.txt        # Python dependencies
│   └── uploads/                # Temporary file storage
│       └── .gitkeep           # Ensures directory exists
│
├── frontend/                   # React frontend application
│   ├── package.json           # Node.js dependencies
│   ├── public/
│   │   ├── index.html         # Main HTML template
│   │   └── manifest.json      # PWA manifest
│   └── src/
│       ├── index.js           # React entry point
│       ├── index.css          # Global styles
│       ├── App.js             # Main application component
│       ├── App.css            # Application styles
│       ├── components/        # React components
│       │   ├── FileUpload.js      # Drag & drop file upload
│       │   ├── FileUpload.css     # Upload component styles
│       │   ├── LoadingSpinner.js  # Processing indicator
│       │   ├── LoadingSpinner.css # Spinner styles
│       │   ├── ResultsDisplay.js  # OCR results display
│       │   └── ResultsDisplay.css # Results styles
│       └── services/          # API integration
│           └── api.js         # API service functions
│
└── sample-images/              # Test images for development
    └── README.md              # Sample images documentation
```

## Key Components

### Backend Architecture

#### `main.py` - FastAPI Application
- **Purpose**: Main API server with endpoints for OCR processing
- **Key Features**:
  - File upload handling with validation
  - Background job processing
  - CORS configuration for frontend integration
  - Health check and status endpoints
  - Error handling and logging

#### `ocr_processor.py` - OCR Engine
- **Purpose**: Core OCR processing using Tesseract
- **Key Features**:
  - Multi-language text extraction
  - Confidence scoring per word
  - PDF multi-page processing
  - Bounding box detection
  - Language auto-detection

#### `image_preprocessor.py` - Image Enhancement
- **Purpose**: Advanced image preprocessing for optimal OCR
- **Key Features**:
  - Automatic image resizing
  - Noise reduction and denoising
  - Skew correction and rotation
  - Contrast enhancement (CLAHE)
  - Adaptive thresholding

#### `models.py` - Data Models
- **Purpose**: Pydantic models for API request/response validation
- **Models**:
  - `OCRResult`: Text extraction results with metadata
  - `BoundingBox`: Word-level positioning and confidence
  - `JobResponse`: Upload confirmation
  - `ResultResponse`: Processing results

#### `config.py` - Configuration Management
- **Purpose**: Centralized configuration with environment variable support
- **Settings**:
  - File size and format limits
  - OCR engine parameters
  - Image processing settings
  - CORS and security settings

### Frontend Architecture

#### `App.js` - Main Application
- **Purpose**: Root component managing application state
- **Features**:
  - File upload orchestration
  - Processing status management
  - Results display coordination
  - Error handling and user feedback

#### `FileUpload.js` - Upload Interface
- **Purpose**: Drag & drop file upload with validation
- **Features**:
  - Multi-file selection
  - Real-time validation feedback
  - Progress indicators
  - Format and size checking

#### `ResultsDisplay.js` - Results Viewer
- **Purpose**: Comprehensive OCR results presentation
- **Features**:
  - Multi-file result navigation
  - Confidence score visualization
  - Text export (copy/download)
  - Bounding box analysis
  - Low-confidence word highlighting

#### `LoadingSpinner.js` - Processing Indicator
- **Purpose**: Visual feedback during OCR processing
- **Features**:
  - Animated progress indicators
  - Processing step visualization
  - Estimated completion feedback

#### `api.js` - API Integration
- **Purpose**: Centralized API communication
- **Features**:
  - File upload with progress
  - Result polling mechanism
  - Error handling and retries
  - Health status monitoring

## Data Flow

### 1. File Upload Process
```
User selects files → FileUpload validates → API uploads → Job created → Background processing starts
```

### 2. OCR Processing Pipeline
```
Raw image → Preprocessing → Language detection → Text extraction → Confidence analysis → Results storage
```

### 3. Results Retrieval
```
Frontend polls API → Job status checked → Results formatted → UI updated → User can export
```

## Configuration Options

### Environment Variables (Backend)
- `DEBUG`: Enable debug mode
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `MAX_FILE_SIZE`: Maximum file size in bytes
- `MAX_BATCH_SIZE`: Maximum files per upload
- `TESSERACT_CONFIG`: OCR engine configuration
- `CORS_ORIGINS`: Allowed frontend origins

### Build Configuration (Frontend)
- `REACT_APP_API_URL`: Backend API URL
- `PUBLIC_URL`: Frontend deployment URL

## Security Considerations

### File Upload Security
- File type validation (extension + MIME type)
- File size limits (10MB default)
- Temporary file cleanup
- Input sanitization

### API Security
- CORS configuration
- Request size limits
- Rate limiting ready (configurable)
- Error message sanitization

## Performance Optimizations

### Backend
- Async file handling
- Background job processing
- Memory-efficient image processing
- Automatic job cleanup

### Frontend
- Component lazy loading
- Efficient re-rendering
- Optimized bundle size
- Progressive image loading

## Scalability Considerations

### Current Implementation
- In-memory job storage
- Local file processing
- Single-server deployment

### Production Enhancements
- Redis for job storage
- Database for persistent data
- Queue system (Celery/RQ)
- Load balancer support
- Container deployment (Docker)
- Cloud storage integration

## Testing Strategy

### Backend Testing
- Unit tests for OCR processing
- Integration tests for API endpoints
- Performance tests for large files
- Error handling validation

### Frontend Testing
- Component unit tests
- User interaction tests
- File upload scenarios
- Error state handling

### End-to-End Testing
- Complete workflow validation
- Multi-file processing
- Error recovery testing
- Performance benchmarking

## Deployment Options

### Local Development
- Use provided startup scripts
- Manual dependency installation
- Direct Python/Node execution

### Production Deployment
- Docker containerization
- Nginx reverse proxy
- PM2 process management
- Cloud platform deployment (AWS, GCP, Azure)

## Monitoring and Logging

### Backend Logging
- Structured logging with levels
- Request/response tracking
- Error stack traces
- Performance metrics

### Frontend Monitoring
- Error boundary implementation
- User interaction tracking
- Performance monitoring
- API call analytics

## Future Enhancements

### Planned Features
- WebSocket real-time updates
- Batch result export
- OCR result editing
- Template-based extraction
- Machine learning improvements

### Integration Possibilities
- Cloud OCR services (AWS Textract, Google Vision)
- Document management systems
- Workflow automation tools
- Mobile application support