#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_gis.settings')
django.setup()

from core.models import User

# Delete if exists
User.objects.filter(username='admin').delete()

# Create superuser
admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
admin.first_name = 'Admin'
admin.last_name = 'User'
admin.save()

print('✅ Admin user created: username=admin, password=admin123')

# Create test user
User.objects.filter(username='testuser').delete()
user = User.objects.create_user('testuser', 'test@example.com', 'test123')
user.first_name = 'Test'
user.last_name = 'User'
user.role = 'USER'
user.profile_completed = True
user.save()

print('✅ Test user created: username=testuser, password=test123')
