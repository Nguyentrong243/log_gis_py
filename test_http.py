#!/usr/bin/env python
"""
Test HTTP requests directly
"""
import urllib.request
import urllib.error
import time

time.sleep(2)  # Wait for server to start

urls = [
    'http://127.0.0.1:8000/',
    'http://127.0.0.1:8000/login/',
    'http://127.0.0.1:8000/register/',
]

print("=" * 60)
print("HTTP Request Tests")
print("=" * 60)

for url in urls:
    try:
        print(f"\nGET {url}")
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.status
            print(f"✅ Status: {status}")
    except urllib.error.HTTPError as e:
        print(f"❌ HTTPError: {e.code}")
        print(f"   {e.reason}")
        try:
            body = e.read().decode('utf-8')
            if '500' in str(e.code):
                # Print first 1000 chars of error
                print(f"   Error details: {body[:1000]}")
        except:
            pass
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 60)
