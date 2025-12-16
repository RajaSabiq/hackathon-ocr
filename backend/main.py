from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import tempfile
import uuid
import logging
import asyncio
from typing import List, Dict, Any
import aiofiles
from pathlib import Path

# Try to import magic, but make it optional
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError:
    MAGIC_AVAILABLE = False
    logger.warning("python-magic not available, MIME type checking will be limited")

from models import JobResponse, ResultResponse, HealthResponse, JobStatus
from ocr_processor import OCRProcessor
import config

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=config.APP_NAME + " API",
    description="Production-ready OCR API for document digitization",
    version=config.APP_VERSION
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OCR processor
ocr_processor = OCRProcessor()

# In-memory job storage (in production, use Redis or database)
job_storage: Dict[str, Dict[str, Any]] = {}

# Create uploads directory
config.UPLOAD_DIR.mkdir(exist_ok=True)

def validate_file(file: UploadFile) -> bool:
    """Validate uploaded file"""
    # Check file extension
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in config.SUPPORTED_EXTENSIONS:
        return False
    
    # Check file size
    if hasattr(file, 'size') and file.size > config.MAX_FILE_SIZE:
        return False
    
    return True

def get_file_type(file_path: str) -> str:
    """Get file MIME type using python-magic"""
    if not MAGIC_AVAILABLE:
        # Fallback to extension-based detection
        ext = Path(file_path).suffix.lower()
        mime_map = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.webp': 'image/webp',
            '.pdf': 'application/pdf'
        }
        return mime_map.get(ext, "unknown")
    
    try:
        mime_type = magic.from_file(file_path, mime=True)
        return mime_type
    except Exception as e:
        logger.warning(f"Could not determine MIME type for {file_path}: {str(e)}")
        return "unknown"

async def save_uploaded_file(file: UploadFile, upload_dir: Path) -> str:
    """Save uploaded file to disk"""
    file_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix.lower()
    file_path = upload_dir / f"{file_id}{file_extension}"
    
    async with aiofiles.open(file_path, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return str(file_path)

async def process_ocr_job(job_id: str, file_paths: List[str], filenames: List[str]):
    """Background task to process OCR job"""
    try:
        logger.info(f"Starting OCR processing for job {job_id}")
        job_storage[job_id]["status"] = JobStatus.PROCESSING
        
        results = []
        errors = []
        
        for file_path, filename in zip(file_paths, filenames):
            try:
                logger.info(f"Processing file: {filename}")
                
                # Validate file type
                mime_type = get_file_type(file_path)
                logger.info(f"Detected MIME type for {filename}: {mime_type}")
                
                if mime_type not in config.SUPPORTED_MIME_TYPES and mime_type != "unknown":
                    error_msg = f"Unsupported MIME type {mime_type} for file {filename}"
                    logger.warning(error_msg)
                    errors.append(error_msg)
                    continue
                
                # Process file
                logger.info(f"Starting OCR for {filename}")
                file_results = ocr_processor.process_file(file_path, filename)
                results.extend(file_results)
                logger.info(f"OCR completed for {filename}: {len(file_results)} results")
                
            except Exception as e:
                error_msg = f"Error processing file {filename}: {str(e)}"
                logger.error(error_msg, exc_info=True)
                errors.append(error_msg)
                # Continue with other files
                continue
            finally:
                # Clean up temporary file
                try:
                    if os.path.exists(file_path):
                        os.unlink(file_path)
                        logger.info(f"Deleted temporary file: {file_path}")
                except Exception as e:
                    logger.warning(f"Could not delete temporary file {file_path}: {str(e)}")
        
        # Update job status
        if results:
            job_storage[job_id]["status"] = JobStatus.COMPLETED
            job_storage[job_id]["results"] = results
            if errors:
                job_storage[job_id]["error_message"] = f"Completed with errors: {'; '.join(errors)}"
            logger.info(f"OCR processing completed for job {job_id}: {len(results)} results")
        else:
            job_storage[job_id]["status"] = JobStatus.FAILED
            job_storage[job_id]["error_message"] = f"No files processed successfully. Errors: {'; '.join(errors)}"
            logger.error(f"OCR processing failed for job {job_id}: no results")
        
    except Exception as e:
        error_msg = f"Critical error in OCR job {job_id}: {str(e)}"
        logger.error(error_msg, exc_info=True)
        job_storage[job_id]["status"] = JobStatus.FAILED
        job_storage[job_id]["error_message"] = error_msg

@app.post("/api/ocr/upload", response_model=JobResponse)
async def upload_documents(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...)
):
    """
    Upload documents for OCR processing
    
    Supports: PNG, JPG, JPEG, WEBP, PDF
    Max file size: 10MB per file
    """
    try:
        logger.info(f"Upload request received with {len(files) if files else 0} files")
        
        if not files:
            logger.error("No files provided in upload request")
            raise HTTPException(status_code=400, detail="No files provided")
        
        if len(files) > config.MAX_BATCH_SIZE:
            logger.error(f"Too many files: {len(files)} > {config.MAX_BATCH_SIZE}")
            raise HTTPException(status_code=400, detail=f"Maximum {config.MAX_BATCH_SIZE} files allowed per batch")
        
        # Validate all files first
        for file in files:
            logger.info(f"Validating file: {file.filename}")
            if not validate_file(file):
                error_msg = f"Invalid file: {file.filename}. Supported formats: PNG, JPG, JPEG, WEBP, PDF (max {config.MAX_FILE_SIZE // (1024*1024)}MB)"
                logger.error(error_msg)
                raise HTTPException(status_code=400, detail=error_msg)
        
        # Generate job ID
        job_id = str(uuid.uuid4())
        logger.info(f"Generated job ID: {job_id}")
        
        # Save files
        file_paths = []
        filenames = []
        
        for file in files:
            try:
                logger.info(f"Saving file: {file.filename}")
                file_path = await save_uploaded_file(file, config.UPLOAD_DIR)
                file_paths.append(file_path)
                filenames.append(file.filename)
                logger.info(f"File saved to: {file_path}")
            except Exception as e:
                logger.error(f"Error saving file {file.filename}: {str(e)}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Error saving file {file.filename}: {str(e)}")
        
        # Initialize job
        job_storage[job_id] = {
            "status": JobStatus.PROCESSING,
            "files_count": len(files),
            "results": [],
            "error_message": None
        }
        
        logger.info(f"Starting background processing for job {job_id}")
        # Start background processing
        background_tasks.add_task(process_ocr_job, job_id, file_paths, filenames)
        
        return JobResponse(
            job_id=job_id,
            status=JobStatus.PROCESSING,
            files_count=len(files)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in upload endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/api/ocr/result/{job_id}", response_model=ResultResponse)
async def get_ocr_result(job_id: str):
    """
    Get OCR processing results for a job
    """
    try:
        if job_id not in job_storage:
            raise HTTPException(status_code=404, detail="Job not found")
        
        job_data = job_storage[job_id]
        
        return ResultResponse(
            job_id=job_id,
            status=job_data["status"],
            results=job_data["results"],
            error_message=job_data.get("error_message")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting result for job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        tesseract_version = ocr_processor.get_tesseract_version()
        
        return HealthResponse(
            status="healthy",
            version="1.0.0",
            tesseract_version=tesseract_version
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

@app.get("/api/supported-formats")
async def get_supported_formats():
    """Get list of supported file formats"""
    return {
        "supported_extensions": list(config.SUPPORTED_EXTENSIONS),
        "supported_mime_types": list(config.SUPPORTED_MIME_TYPES),
        "max_file_size_mb": config.MAX_FILE_SIZE // (1024 * 1024),
        "max_batch_size": config.MAX_BATCH_SIZE
    }

@app.delete("/api/ocr/job/{job_id}")
async def delete_job(job_id: str):
    """Delete a job and its results"""
    try:
        if job_id not in job_storage:
            raise HTTPException(status_code=404, detail="Job not found")
        
        del job_storage[job_id]
        
        return {"message": "Job deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting job {job_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Cleanup old jobs periodically (simple implementation)
async def cleanup_old_jobs():
    """Clean up jobs older than 1 hour"""
    import time
    current_time = time.time()
    
    jobs_to_delete = []
    for job_id, job_data in job_storage.items():
        # This is a simplified cleanup - in production, store timestamps
        if len(job_storage) > config.MAX_JOBS_IN_MEMORY:  # Keep only recent jobs
            jobs_to_delete.append(job_id)
    
    for job_id in jobs_to_delete[:config.JOB_CLEANUP_BATCH_SIZE]:  # Delete oldest batch
        del job_storage[job_id]

@app.on_event("startup")
async def startup_event():
    """Application startup"""
    logger.info("OCR API starting up...")
    logger.info(f"Tesseract version: {ocr_processor.get_tesseract_version()}")
    logger.info(f"Supported languages: {len(ocr_processor.supported_languages)}")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    logger.info("OCR API shutting down...")
    
    # Clean up any remaining temporary files
    try:
        for file_path in config.UPLOAD_DIR.glob("*"):
            if file_path.is_file():
                file_path.unlink()
    except Exception as e:
        logger.warning(f"Error cleaning up temporary files: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=config.RELOAD,
        log_level=config.LOG_LEVEL.lower()
    )