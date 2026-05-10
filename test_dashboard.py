#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify the admin dashboard loads correctly with SingleOrder section
"""
import os
import sys
import django

# Fix encoding for Windows
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_gis.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

# Create test client
client = Client()

# Get or create admin user
admin_users = User.objects.filter(is_superuser=True)
if admin_users.exists():
    admin_user = admin_users.first()
    print(f"✓ Using existing admin user: {admin_user.username}")
else:
    admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print(f"✓ Created admin user: {admin_user.username}")

# Login
client.login(username=admin_user.username, password='admin123')
print("✓ Logged in as admin")

# Request the dashboard
response = client.get('/admin-dashboard/')
print(f"\n✓ Dashboard response status: {response.status_code}")

if response.status_code == 200:
    content = response.content.decode('utf-8')
    
    # Check for key elements
    checks = [
        ('Quản Lý Đơn Lẻ', 'Single Order Management section title'),
        ('singleOrderSearch', 'Single Order search box'),
        ('badge-pending', 'Pending badge CSS class'),
        ('badge-approved', 'Approved badge CSS class'),
        ('badge-in_progress', 'In Progress badge CSS class'),
        ('badge-delivered', 'Delivered badge CSS class'),
        ('badge-cancelled', 'Cancelled badge CSS class'),
        ('filterSingleOrders', 'Filter function'),
        ('viewSingleOrderTracking', 'Tracking function'),
        ('editSingleOrder', 'Edit function'),
    ]
    
    print("\n✓ Content checks:")
    for keyword, description in checks:
        if keyword in content:
            print(f"  ✓ {description}")
        else:
            print(f"  ✗ MISSING: {description}")
    
    print("\n✓ Dashboard loads successfully!")
else:
    print(f"✗ Dashboard returned status {response.status_code}")
    print(response.content[:500].decode('utf-8', errors='ignore'))
