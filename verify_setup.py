import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_gis.settings')
django.setup()

from core.models import User, Vehicle, Warehouse, Order

print("\n✅ DATABASE CHECK:\n")

# Check admin
admin = User.objects.filter(username='admin123').first()
if admin:
    print(f"✓ Admin user exists")
    print(f"  - Username: {admin.username}")
    print(f"  - Role: {admin.role}")
    print(f"  - Active: {admin.is_active}")
else:
    print("✗ Admin user NOT found - creating...")
    admin = User.objects.create_user(
        username='admin123',
        email='admin@logistics.vn',
        password='admin123',
        role='ADMIN'
    )
    print(f"✓ Created admin: {admin.username}")

# Check sample data
vehicles = Vehicle.objects.count()
warehouses = Warehouse.objects.count()
orders = Order.objects.count()

print(f"\n✓ Sample data:")
print(f"  - {vehicles} Vehicles")
print(f"  - {warehouses} Warehouses")
print(f"  - {orders} Orders")

print(f"\n✅ Ready to access:")
print(f"  - Login: http://localhost:8000/login/")
print(f"  - Username: admin123")
print(f"  - Password: admin123")
print(f"  - Dashboard: http://localhost:8000/admin-dashboard/\n")
