#!/usr/bin/env python3
"""
Test if the backend can start without errors
"""

import sys
import os

print("Testing backend startup...")
print("=" * 50)

try:
    print("\n1. Testing imports...")
    from fastapi import FastAPI
    from models import JobResponse, ResultResponse, HealthResponse, JobStatus
    import config
    print("   ✓ Core imports successful")
    
    print("\n2. Testing OCR processor initialization...")
    from ocr_processor import OCRProcessor
    processor = OCRProcessor()
    print("   ✓ OCR processor initialized")
    
    print("\n3. Getting Tesseract version...")
    version = processor.get_tesseract_version()
    print(f"   Tesseract version: {version}")
    
    if "3." in version or "3.0" in version:
        print("\n   ⚠️  WARNING: Tesseract 3.x detected!")
        print("   ⚠️  This version is very old (2011) and may cause issues")
        print("   ⚠️  Recommended: Upgrade to Tesseract 5.x")
        print("   ⚠️  Download: https://github.com/UB-Mannheim/tesseract/wiki")
        print("\n   The application may still work but with reduced functionality.")
    
    print("\n4. Testing configuration...")
    print(f"   Upload dir: {config.UPLOAD_DIR}")
    print(f"   Max file size: {config.MAX_FILE_SIZE // (1024*1024)}MB")
    print(f"   Host: {config.HOST}:{config.PORT}")
    
    print("\n5. Creating upload directory...")
    config.UPLOAD_DIR.mkdir(exist_ok=True)
    print(f"   ✓ Upload directory ready: {config.UPLOAD_DIR}")
    
    print("\n" + "=" * 50)
    print("✅ Backend can start!")
    print("=" * 50)
    print("\nTo start the server, run:")
    print("  python main.py")
    print("\nThen test with:")
    print("  curl http://localhost:8000/api/health")
    
except Exception as e:
    print(f"\n❌ Error during startup test: {e}")
    import traceback
    traceback.print_exc()
    print("\n" + "=" * 50)
    print("❌ Backend cannot start!")
    print("=" * 50)
    print("\nPlease fix the errors above before starting the server.")
    sys.exit(1)
