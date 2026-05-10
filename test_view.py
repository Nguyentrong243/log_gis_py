#!/usr/bin/env python
"""
Simple view test
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_gis.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.forms import AuthenticationForm
from core.views import CustomLoginView

print("=" * 60)
print("TEST: CustomLoginView")
print("=" * 60)

# Create a test request
factory = RequestFactory()
request = factory.get('/login/')

# Create view instance
view = CustomLoginView()

# Check if form_class is set
print(f"View class: {view.__class__.__name__}")
print(f"Form class: {view.form_class}")
print(f"Template name: {view.template_name}")

# Try to get context
try:
    view.request = request
    context = view.get_context_data()
    print(f"✅ Context data obtained")
    print(f"   Keys: {list(context.keys())}")
    if 'form' in context:
        print(f"✅ Form in context: {context['form'].__class__.__name__}")
    else:
        print(f"❌ Form NOT in context")
except Exception as e:
    print(f"❌ Error getting context: {e}")

print("=" * 60)
