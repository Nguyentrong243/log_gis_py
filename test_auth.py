#!/usr/bin/env python
"""
Test script để kiểm tra login/register
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_gis.settings')
django.setup()

from django.contrib.auth import authenticate
from core.models import User

# Test 1: Check admin user exists
print("=" * 60)
print("TEST 1: Check users exist")
print("=" * 60)

admin = User.objects.filter(username='admin').first()
if admin:
    print(f"✅ Admin user found: {admin.username}, email={admin.email}, is_superuser={admin.is_superuser}")
else:
    print("❌ Admin user NOT found")

testuser = User.objects.filter(username='testuser').first()
if testuser:
    print(f"✅ Test user found: {testuser.username}, email={testuser.email}, role={testuser.role}")
else:
    print("❌ Test user NOT found")

# Test 2: Try to authenticate
print("\n" + "=" * 60)
print("TEST 2: Test authentication")
print("=" * 60)

user = authenticate(username='admin', password='admin123')
if user is not None:
    print(f"✅ Admin authentication successful")
else:
    print(f"❌ Admin authentication FAILED")

user = authenticate(username='testuser', password='test123')
if user is not None:
    print(f"✅ Test user authentication successful")
else:
    print(f"❌ Test user authentication FAILED")

# Test 3: Check forms
print("\n" + "=" * 60)
print("TEST 3: Test CustomUserCreationForm")
print("=" * 60)

from core.forms import CustomUserCreationForm

form_data = {
    'username': 'newuser',
    'email': 'newuser@test.com',
    'password1': 'TestPassword123!',
    'password2': 'TestPassword123!',
}

form = CustomUserCreationForm(data=form_data)
if form.is_valid():
    print(f"✅ Form is valid")
else:
    print(f"❌ Form has errors: {form.errors}")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)
 