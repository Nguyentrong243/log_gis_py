#!/usr/bin/env python
"""
Test script to verify admin dashboard access
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_gis.settings')
django.setup()

from core.models import User

# Check admin user
print("=" * 60)
print("ADMIN DASHBOARD ACCESS TEST")
print("=" * 60)

admin = User.objects.filter(username='admin123').first()

if admin:
    print(f"\n✓ Admin user found: {admin.username}")
    print(f"  - Email: {admin.email}")
    print(f"  - Role: {admin.role}")
    print(f"  - Has ADMIN role: {admin.role == 'ADMIN'}")
    print(f"  - Is Active: {admin.is_active}")
    print(f"  - Is Staff: {admin.is_staff}")
    
    if admin.role == 'ADMIN':
        print("\n✓ Admin can access /admin-dashboard/")
        print(f"\n📊 Dashboard will show:")
        
        from core.models import Vehicle, Warehouse, Order, OrderTracking
        
        vehicles = Vehicle.objects.all().count()
        warehouses = Warehouse.objects.all().count()
        orders = Order.objects.all().count()
        trackings = OrderTracking.objects.all().count()
        
        print(f"   - {vehicles} Vehicles")
        print(f"   - {warehouses} Warehouses")
        print(f"   - {orders} Orders")
        print(f"   - {trackings} Order Trackings")
        
        print("\n🔐 Login with:")
        print(f"   Username: {admin.username}")
        print(f"   Password: (use your password)")
        
        print("\n📍 Then go to: http://localhost:8000/admin-dashboard/")
        
    else:
        print(f"\n✗ ERROR: Admin has role '{admin.role}' instead of 'ADMIN'")
else:
    print("\n✗ Admin user 'admin123' not found!")
    print("   Please run: python create_sample_data.py")

print("\n" + "=" * 60)
