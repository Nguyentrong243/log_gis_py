#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django
import traceback

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_gis.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

try:
    client = Client()
    
    # Get or create admin
    admin_users = User.objects.filter(is_superuser=True)
    if admin_users.exists():
        admin_user = admin_users.first()
        print(f"Admin user: {admin_user.username}")
    else:
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print(f"Created admin: {admin_user.username}")
    
    # Try login
    login_result = client.login(username=admin_user.username, password='admin123')
    print(f"Login result: {login_result}")
    
    # Try access dashboard
    response = client.get('/admin-dashboard/')
    print(f"\nResponse status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"Error content:\n{response.content.decode('utf-8', errors='ignore')[:1000]}")
    else:
        content = response.content.decode('utf-8')
        if 'Quản Lý Đơn Lẻ' in content:
            print("✓ Dashboard loaded successfully!")
        else:
            print("✗ Dashboard missing Single Order section")
            
except Exception as e:
    print(f"Exception occurred: {e}")
    traceback.print_exc()
