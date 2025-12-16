#!/usr/bin/env python3
"""Quick test of backend health endpoint"""

import requests
import time
import sys

print("Testing backend health endpoint...")
print("=" * 50)

# Wait a moment for backend to fully start
time.sleep(2)

try:
    print("\n1. Testing http://localhost:8000/api/health")
    response = requests.get("http://localhost:8000/api/health", timeout=5)
    
    print(f"   Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ SUCCESS!")
        print(f"\n   Response:")
        print(f"   {data}")
        print(f"\n   Status: {data.get('status')}")
        print(f"   Version: {data.get('version')}")
        print(f"   Tesseract: {data.get('tesseract_version')}")
        print("\n" + "=" * 50)
        print("✅ Backend is working correctly!")
        print("=" * 50)
        sys.exit(0)
    else:
        print(f"   ❌ FAILED with status {response.status_code}")
        print(f"   Response: {response.text}")
        sys.exit(1)
        
except requests.exceptions.ConnectionError as e:
    print(f"   ❌ CONNECTION ERROR")
    print(f"   Cannot connect to backend at http://localhost:8000")
    print(f"\n   Possible causes:")
    print(f"   - Backend is not running")
    print(f"   - Backend is starting on a different port")
    print(f"   - Firewall is blocking the connection")
    print(f"\n   Error details: {e}")
    sys.exit(1)
    
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    sys.exit(1)
