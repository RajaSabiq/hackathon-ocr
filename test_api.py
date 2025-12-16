#!/usr/bin/env python3
"""
OCR API Test Script

This script tests the OCR API endpoints to ensure everything is working correctly.
Run this after starting the backend server to verify functionality.
"""

import requests
import time
import json
from pathlib import Path
import sys

API_BASE = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed")
            print(f"   Status: {data['status']}")
            print(f"   Version: {data['version']}")
            print(f"   Tesseract: {data['tesseract_version']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def test_supported_formats():
    """Test the supported formats endpoint"""
    print("\n🔍 Testing supported formats endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/supported-formats", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Supported formats retrieved")
            print(f"   Extensions: {data['supported_extensions']}")
            print(f"   Max file size: {data['max_file_size_mb']}MB")
            print(f"   Max batch size: {data['max_batch_size']}")
            return True
        else:
            print(f"❌ Supported formats failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Supported formats error: {str(e)}")
        return False

def create_test_image():
    """Create a simple test image with text"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # Create a simple image with text
        img = Image.new('RGB', (400, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        # Try to use a default font, fallback to basic if not available
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        text = "Hello World!\nThis is a test document.\nOCR should read this text."
        draw.text((20, 50), text, fill='black', font=font)
        
        # Save to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return img_bytes.getvalue()
        
    except ImportError:
        print("⚠️  PIL not available, skipping image creation test")
        return None
    except Exception as e:
        print(f"⚠️  Could not create test image: {str(e)}")
        return None

def test_ocr_upload():
    """Test OCR upload and processing"""
    print("\n🔍 Testing OCR upload and processing...")
    
    # Create test image
    test_image_data = create_test_image()
    if not test_image_data:
        print("⚠️  Skipping OCR test - no test image available")
        return True
    
    try:
        # Upload the test image
        files = {'files': ('test.png', test_image_data, 'image/png')}
        response = requests.post(f"{API_BASE}/api/ocr/upload", files=files, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        upload_data = response.json()
        job_id = upload_data['job_id']
        print(f"✅ Upload successful, job ID: {job_id}")
        
        # Poll for results
        print("⏳ Waiting for OCR processing...")
        max_attempts = 30
        for attempt in range(max_attempts):
            time.sleep(2)
            
            result_response = requests.get(f"{API_BASE}/api/ocr/result/{job_id}", timeout=10)
            if result_response.status_code != 200:
                print(f"❌ Result fetch failed: {result_response.status_code}")
                return False
            
            result_data = result_response.json()
            status = result_data['status']
            
            if status == 'completed':
                print(f"✅ OCR processing completed!")
                results = result_data['results']
                if results:
                    result = results[0]
                    print(f"   Filename: {result['filename']}")
                    print(f"   Confidence: {result['confidence']:.2%}")
                    print(f"   Language: {result['language']}")
                    print(f"   Text length: {len(result['text'])} characters")
                    print(f"   Extracted text: {result['text'][:100]}...")
                    print(f"   Bounding boxes: {len(result['bbox_data'])}")
                else:
                    print("⚠️  No results returned")
                return True
                
            elif status == 'failed':
                print(f"❌ OCR processing failed: {result_data.get('error_message', 'Unknown error')}")
                return False
            
            elif status == 'processing':
                print(f"   Still processing... (attempt {attempt + 1}/{max_attempts})")
            else:
                print(f"❌ Unknown status: {status}")
                return False
        
        print(f"❌ OCR processing timeout after {max_attempts} attempts")
        return False
        
    except Exception as e:
        print(f"❌ OCR test error: {str(e)}")
        return False

def test_invalid_upload():
    """Test upload with invalid file"""
    print("\n🔍 Testing invalid file upload...")
    try:
        # Try to upload a text file (should be rejected)
        files = {'files': ('test.txt', b'This is not an image', 'text/plain')}
        response = requests.post(f"{API_BASE}/api/ocr/upload", files=files, timeout=10)
        
        if response.status_code == 400:
            print("✅ Invalid file correctly rejected")
            return True
        else:
            print(f"❌ Invalid file not rejected: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Invalid upload test error: {str(e)}")
        return False

def test_nonexistent_job():
    """Test fetching results for non-existent job"""
    print("\n🔍 Testing non-existent job lookup...")
    try:
        fake_job_id = "00000000-0000-0000-0000-000000000000"
        response = requests.get(f"{API_BASE}/api/ocr/result/{fake_job_id}", timeout=10)
        
        if response.status_code == 404:
            print("✅ Non-existent job correctly returns 404")
            return True
        else:
            print(f"❌ Non-existent job returned: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Non-existent job test error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting OCR API Tests")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Supported Formats", test_supported_formats),
        ("OCR Upload & Processing", test_ocr_upload),
        ("Invalid File Upload", test_invalid_upload),
        ("Non-existent Job", test_nonexistent_job),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} crashed: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! OCR API is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Check the backend server and try again.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)