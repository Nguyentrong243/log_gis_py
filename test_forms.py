#!/usr/bin/env python
"""
Test login form submission
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_gis.settings')
django.setup()

from django.test import Client
from django.urls import reverse

client = Client()

print("=" * 60)
print("TEST: Login Form Submission")
print("=" * 60)

# Test 1: GET login page
print("\n1. GET /login/")
response = client.get('/login/')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   ✅ Login page loads")
else:
    print(f"   ❌ Login page failed: {response.status_code}")
    print(f"   Content: {response.content[:500]}")

# Test 2: POST login with correct credentials
print("\n2. POST /login/ with admin credentials")
response = client.post('/login/', {
    'username': 'admin',
    'password': 'admin123'
}, follow=True)
print(f"   Status: {response.status_code}")
print(f"   Final URL: {response.redirect_chain}")
if response.status_code == 200:
    print(f"   ✅ Login processed")
else:
    print(f"   ❌ Login failed")
    if hasattr(response, 'context') and response.context:
        if 'form' in response.context:
            form = response.context['form']
            print(f"   Form errors: {form.errors}")

# Test 3: GET register page
print("\n3. GET /register/")
response = client.get('/register/')
print(f"   Status: {response.status_code}")
if response.status_code == 200:
    print(f"   ✅ Register page loads")
else:
    print(f"   ❌ Register page failed")

# Test 4: POST register
print("\n4. POST /register/ with new user")
response = client.post('/register/', {
    'username': 'newuser123',
    'email': 'newuser@test.com',
    'password1': 'TestPass123!@',
    'password2': 'TestPass123!@'
}, follow=True)
print(f"   Status: {response.status_code}")
print(f"   Redirect chain: {response.redirect_chain}")
if response.status_code == 200:
    print(f"   ✅ Register form processed")
else:
    print(f"   ❌ Register failed")
    if hasattr(response, 'context') and response.context:
        if 'form' in response.context:
            form = response.context['form']
            print(f"   Form errors: {form.errors}")

print("\n" + "=" * 60)
