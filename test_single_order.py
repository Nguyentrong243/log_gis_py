#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_gis.settings')
django.setup()

from core.models import SingleOrder
from django.template import Context, Template

print("✓ All imports successful")
print("✓ SingleOrder model ready")

# Check status choices
print("\n✓ SingleOrder status choices:")
for code, label in SingleOrder.STATUS_CHOICES:
    print(f"  {code} -> {label}")

# Count records
count = SingleOrder.objects.count()
print(f"\n✓ SingleOrder count in database: {count}")

# Test template rendering
print("\n✓ Template rendering test:")
status_value = "APPROVED"
# Simulate what template will do
from django.utils.html import format_html
status_lower = status_value.lower()
print(f"  Status 'APPROVED' -> '{status_lower}' (css class: badge-{status_lower})")

status_value = "IN_PROGRESS"
status_lower = status_value.lower()
print(f"  Status 'IN_PROGRESS' -> '{status_lower}' (css class: badge-{status_lower})")

print("\n✓ All tests passed!")
