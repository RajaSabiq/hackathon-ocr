import os
from pathlib import Path

# Application settings
APP_NAME = "OCR Document Digitizer"
APP_VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Server settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
RELOAD = DEBUG

# File upload settings
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))  # 10MB
MAX_BATCH_SIZE = int(os.getenv("MAX_BATCH_SIZE", 10))
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "uploads"))

# Supported file types
SUPPORTED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.pdf'}
SUPPORTED_MIME_TYPES = {
    'image/png', 'image/jpeg', 'image/jpg', 'image/webp', 
    'application/pdf'
}

# OCR settings
# Tesseract config compatible with version 3.x (no --oem flag)
# PSM 6 = Assume a single uniform block of text
TESSERACT_CONFIG = os.getenv(
    "TESSERACT_CONFIG", 
    r'--psm 6'
)

# Image preprocessing settings
MAX_IMAGE_DIMENSION = int(os.getenv("MAX_IMAGE_DIMENSION", 3000))
MIN_IMAGE_DIMENSION = int(os.getenv("MIN_IMAGE_DIMENSION", 300))
PDF_DPI = int(os.getenv("PDF_DPI", 300))

# CORS settings
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

# Logging settings
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Job cleanup settings
MAX_JOBS_IN_MEMORY = int(os.getenv("MAX_JOBS_IN_MEMORY", 100))
JOB_CLEANUP_BATCH_SIZE = int(os.getenv("JOB_CLEANUP_BATCH_SIZE", 50))