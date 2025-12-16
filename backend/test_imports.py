#!/usr/bin/env python3
"""
Test script to verify all imports and dependencies are working
"""

import sys

print("Testing imports...")

try:
    print("✓ Testing FastAPI...")
    from fastapi import FastAPI
    print("  FastAPI imported successfully")
except ImportError as e:
    print(f"✗ FastAPI import failed: {e}")
    sys.exit(1)

try:
    print("✓ Testing pytesseract...")
    import pytesseract
    version = pytesseract.get_tesseract_version()
    print(f"  Tesseract version: {version}")
except Exception as e:
    print(f"✗ Tesseract import/check failed: {e}")
    print("  Make sure Tesseract OCR is installed and in PATH")
    sys.exit(1)

try:
    print("✓ Testing OpenCV...")
    import cv2
    print(f"  OpenCV version: {cv2.__version__}")
except ImportError as e:
    print(f"✗ OpenCV import failed: {e}")
    sys.exit(1)

try:
    print("✓ Testing PIL...")
    from PIL import Image
    print("  PIL imported successfully")
except ImportError as e:
    print(f"✗ PIL import failed: {e}")
    sys.exit(1)

try:
    print("✓ Testing pdf2image...")
    from pdf2image import convert_from_path
    print("  pdf2image imported successfully")
except ImportError as e:
    print(f"✗ pdf2image import failed: {e}")
    sys.exit(1)

try:
    print("✓ Testing python-magic...")
    import magic
    print("  python-magic imported successfully")
except ImportError as e:
    print(f"⚠ python-magic import failed: {e}")
    print("  This is optional - will use fallback MIME detection")

try:
    print("✓ Testing config...")
    import config
    print(f"  Upload dir: {config.UPLOAD_DIR}")
    print(f"  Max file size: {config.MAX_FILE_SIZE // (1024*1024)}MB")
    print(f"  Tesseract config: {config.TESSERACT_CONFIG}")
except Exception as e:
    print(f"✗ Config import failed: {e}")
    sys.exit(1)

try:
    print("✓ Testing models...")
    from models import OCRResult, JobResponse
    print("  Models imported successfully")
except Exception as e:
    print(f"✗ Models import failed: {e}")
    sys.exit(1)

try:
    print("✓ Testing image_preprocessor...")
    from image_preprocessor import ImagePreprocessor
    preprocessor = ImagePreprocessor()
    print("  ImagePreprocessor initialized successfully")
except Exception as e:
    print(f"✗ ImagePreprocessor import failed: {e}")
    sys.exit(1)

try:
    print("✓ Testing ocr_processor...")
    from ocr_processor import OCRProcessor
    processor = OCRProcessor()
    print(f"  OCRProcessor initialized successfully")
    print(f"  Supported languages: {len(processor.supported_languages)}")
except Exception as e:
    print(f"✗ OCRProcessor import failed: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("✅ All imports successful!")
print("="*50)
print("\nYou can now start the backend server with:")
print("  python main.py")
