import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_gis.settings')
django.setup()

from django.utils import timezone
from core.models import Warehouse, Vehicle, User, Order, OrderTracking, OrderTrackingLog, SingleOrder

def create_sample_data():
    print("🚀 Tạo dữ liệu mẫu cho hệ thống...\n")
    
    # ============================================================================
    # 1. CREATE WAREHOUSES
    # ============================================================================
    print("📦 Tạo kho bãi...")
    warehouses_data = [
        {
            'name': 'Kho TPHCM (Tân Phú)',
            'address': '123 Đường Lê Đại Hành, Tân Phú, TPHCM',
            'manager_name': 'Nguyễn Văn Tuấn',
            'manager_phone': '0908123456',
            'lat': 10.762622,
            'lng': 106.660172,
        },
        {
            'name': 'Kho Hải Dương (Chợ Mơi)',
            'address': '456 Đường Hoàng Văn Thụ, Chợ Mơi, Hải Dương',
            'manager_name': 'Trần Thị Thu Hà',
            'manager_phone': '0918234567',
            'lat': 20.941108,
            'lng': 106.332098,
        },
        {
            'name': 'Kho Hà Nội (Thanh Xuân)',
            'address': '789 Đường Phạm Văn Đồng, Thanh Xuân, Hà Nội',
            'manager_name': 'Phạm Quốc Anh',
            'manager_phone': '0938345678',
            'lat': 21.002142,
            'lng': 105.847381,
        },
        {
            'name': 'Kho Nam Định (Thành Phố)',
            'address': '321 Đường Lê Duẩn, Thành Phố Nam Định',
            'manager_name': 'Vũ Thị Lan',
            'manager_phone': '0948456789',
            'lat': 20.422792,
            'lng': 105.778893,
        },
    ]
    
    warehouses = {}
    for wh_data in warehouses_data:
        wh, created = Warehouse.objects.get_or_create(
            name=wh_data['name'],
            defaults=wh_data
        )
        warehouses[wh_data['name']] = wh
        status = "✓ Tạo mới" if created else "✓ Đã tồn tại"
        print(f"  {status}: {wh_data['name']}")
    
    # ============================================================================
    # 2. CREATE DRIVERS
    # ============================================================================
    print("\n👨 Tạo tài xế...")
    drivers_data = [
        {
            'username': 'driver001',
            'first_name': 'Nguyễn',
            'last_name': 'Văn A',
            'email': 'driver001@logistics.vn',
            'phone_number': '0908111111',
            'id_card_number': '123456789012',
            'date_of_birth': datetime(1988, 5, 15).date(),
            'address': '123 Đường Nguyễn Huệ, TPHCM',
            'password': 'driver123',
        },
        {
            'username': 'driver002',
            'first_name': 'Trần',
            'last_name': 'Thị B',
            'email': 'driver002@logistics.vn',
            'phone_number': '0918222222',
            'id_card_number': '234567890123',
            'date_of_birth': datetime(1990, 8, 22).date(),
            'address': '456 Đường Lê Lợi, Hải Dương',
            'password': 'driver123',
        },
        {
            'username': 'driver003',
            'first_name': 'Phạm',
            'last_name': 'Văn C',
            'email': 'driver003@logistics.vn',
            'phone_number': '0938333333',
            'id_card_number': '345678901234',
            'date_of_birth': datetime(1992, 3, 10).date(),
            'address': '789 Đường Hoàng Việt, Hà Nội',
            'password': 'driver123',
        },
        {
            'username': 'driver004',
            'first_name': 'Vũ',
            'last_name': 'Thị D',
            'email': 'driver004@logistics.vn',
            'phone_number': '0948444444',
            'id_card_number': '456789012345',
            'date_of_birth': datetime(1995, 11, 28).date(),
            'address': '321 Đường Trần Hưng Đạo, Nam Định',
            'password': 'driver123',
        },
    ]
    
    drivers = {}
    for driver_data in drivers_data:
        password = driver_data.pop('password')
        driver, created = User.objects.get_or_create(
            username=driver_data['username'],
            defaults={**driver_data, 'role': 'DRIVER', 'driver_status': 'ONLINE'}
        )
        if created:
            driver.set_password(password)
            driver.save()
        drivers[driver_data['username']] = driver
        status = "✓ Tạo mới" if created else "✓ Đã tồn tại"
        print(f"  {status}: {driver_data['first_name']} {driver_data['last_name']}")
    
    # ============================================================================
    # 3. CREATE VEHICLES
    # ============================================================================
    print("\n🚗 Tạo phương tiện...")
    vehicles_data = [
        {
            'name': 'Xe Tải Nhỏ 01',
            'driver_name': 'Nguyễn Văn A',
            'driver_birth_year': 1988,
            'plate_number': '51A-12345',
            'vehicle_type': 'Xe Tải Nhỏ',
            'lat': 10.762622,
            'lng': 106.660172,
            'status': 'ACTIVE',
        },
        {
            'name': 'Xe Van 02',
            'driver_name': 'Trần Thị B',
            'driver_birth_year': 1990,
            'plate_number': '51B-54321',
            'vehicle_type': 'Xe Van',
            'lat': 10.752622,
            'lng': 106.650172,
            'status': 'ACTIVE',
        },
        {
            'name': 'Xe Tải Vừa 03',
            'driver_name': 'Phạm Văn C',
            'driver_birth_year': 1992,
            'plate_number': '51C-78901',
            'vehicle_type': 'Xe Tải Vừa',
            'lat': 20.941108,
            'lng': 106.332098,
            'status': 'ON_DELIVERY',
        },
        {
            'name': 'Xe Tải Lớn 04',
            'driver_name': 'Vũ Thị D',
            'driver_birth_year': 1995,
            'plate_number': '51D-34567',
            'vehicle_type': 'Xe Tải Lớn',
            'lat': 21.002142,
            'lng': 105.847381,
            'status': 'ACTIVE',
        },
    ]
    
    vehicles = {}
    for vehicle_data in vehicles_data:
        vehicle, created = Vehicle.objects.get_or_create(
            plate_number=vehicle_data['plate_number'],
            defaults=vehicle_data
        )
        vehicles[vehicle_data['plate_number']] = vehicle
        status = "✓ Tạo mới" if created else "✓ Đã tồn tại"
        print(f"  {status}: {vehicle_data['name']} - {vehicle_data['plate_number']}")
    
    # ============================================================================
    # 4. CREATE ADMIN USER
    # ============================================================================
    print("\n👑 Tạo tài khoản Admin...")
    admin, created = User.objects.get_or_create(
        username='admin123',
        defaults={
            'first_name': 'Admin',
            'last_name': 'Logistics',
            'email': 'admin@logistics.vn',
            'role': 'ADMIN',
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print(f"  ✓ Tạo mới: admin123 (Mật khẩu: admin123)")
    else:
        print(f"  ✓ Đã tồn tại: admin123")
    
    # ============================================================================
    # 5. CREATE ORDERS WITH MULTI-WAREHOUSE TRACKING
    # ============================================================================
    print("\n📋 Tạo đơn hàng với multi-warehouse tracking...")
    
    # Order 1: TPHCM -> Hải Dương -> Hà Nội -> Nam Định
    order1, created = Order.objects.get_or_create(
        code='LOG-2026-0001',
        defaults={
            'customer_name': 'Cửa hàng Nguyễn Hàng',
            'customer_phone': '0901111111',
            'pickup_point': 'Kho TPHCM (Tân Phú)',
            'delivery_point': 'Cửa hàng Nguyễn, 654 Đường Lê Duẩn, Nam Định',
            'product_type': 'FASHION',
            'product_size': 'LARGE',
            'base_price': 500000,
            'total_price': 500000,
            'status': 'IN_PROGRESS',
            'created_by': admin,
        }
    )
    
    if created:
        # Create tracking for each warehouse
        wh1 = warehouses['Kho TPHCM (Tân Phú)']
        wh2 = warehouses['Kho Hải Dương (Chợ Mơi)']
        wh3 = warehouses['Kho Hà Nội (Thanh Xuân)']
        wh4 = warehouses['Kho Nam Định (Thành Phố)']
        
        # Tracking 1: Tại kho TPHCM - CHECKED_IN
        track1 = OrderTracking.objects.create(
            order=order1,
            warehouse=wh1,
            sequence=1,
            status='CHECKED_IN',
            checked_in_at=timezone.now() - timedelta(hours=2),
            checked_in_by=admin,
            notes='Hàng đã được kiểm tra và sẵn sàng vận chuyển'
        )
        OrderTrackingLog.objects.create(
            order=order1,
            warehouse=wh1,
            action='CHECK_IN',
            user=admin,
            notes='Đã check-in tại kho TPHCM'
        )
        
        # Tracking 2: Tại kho Hải Dương - PENDING
        track2 = OrderTracking.objects.create(
            order=order1,
            warehouse=wh2,
            sequence=2,
            status='PENDING',
            notes='Chờ xe đến'
        )
        
        # Tracking 3: Tại kho Hà Nội - PENDING
        track3 = OrderTracking.objects.create(
            order=order1,
            warehouse=wh3,
            sequence=3,
            status='PENDING',
        )
        
        # Tracking 4: Tại kho Nam Định - PENDING
        track4 = OrderTracking.objects.create(
            order=order1,
            warehouse=wh4,
            sequence=4,
            status='PENDING',
        )
        
        print(f"  ✓ Tạo mới: {order1.code} - TPHCM → Hải Dương → Hà Nội → Nam Định")
    
    # Order 2: TPHCM -> Hà Nội (đã giao)
    order2, created = Order.objects.get_or_create(
        code='LOG-2026-0002',
        defaults={
            'customer_name': 'Công ty ABC Trading',
            'customer_phone': '0902222222',
            'pickup_point': 'Kho TPHCM (Tân Phú)',
            'delivery_point': 'Công ty ABC, 111 Đường Đinh Tiên Hoàng, Hà Nội',
            'product_type': 'ELECTRONICS',
            'product_size': 'MEDIUM',
            'base_price': 750000,
            'total_price': 750000,
            'status': 'DELIVERED',
            'created_by': admin,
        }
    )
    
    if created:
        wh1 = warehouses['Kho TPHCM (Tân Phú)']
        wh3 = warehouses['Kho Hà Nội (Thanh Xuân)']
        
        # Tracking 1: DELIVERED
        OrderTracking.objects.create(
            order=order2,
            warehouse=wh1,
            sequence=1,
            status='DELIVERED',
            checked_in_at=timezone.now() - timedelta(hours=8),
            checked_in_by=admin,
            notes='Đã vận chuyển đến Hà Nội'
        )
        OrderTrackingLog.objects.create(
            order=order2,
            warehouse=wh1,
            action='CHECK_IN',
            user=admin,
            notes='Đã check-in tại kho TPHCM'
        )
        
        # Tracking 2: DELIVERED
        OrderTracking.objects.create(
            order=order2,
            warehouse=wh3,
            sequence=2,
            status='DELIVERED',
            checked_in_at=timezone.now() - timedelta(hours=2),
            checked_in_by=admin,
            notes='Giao hàng thành công'
        )
        OrderTrackingLog.objects.create(
            order=order2,
            warehouse=wh3,
            action='DELIVERED',
            user=admin,
            notes='Giao hàng cho khách hàng thành công'
        )
        
        print(f"  ✓ Tạo mới: {order2.code} - TPHCM → Hà Nội (Đã giao)")
    
    # Order 3: PENDING
    order3, created = Order.objects.get_or_create(
        code='LOG-2026-0003',
        defaults={
            'customer_name': 'Siêu thị Mart',
            'customer_phone': '0903333333',
            'pickup_point': 'Kho TPHCM (Tân Phú)',
            'delivery_point': 'Siêu thị Mart, 999 Đường Nguyễn Kiếm, Hà Nội',
            'product_type': 'HOUSEHOLD',
            'product_size': 'LARGE',
            'base_price': 600000,
            'total_price': 600000,
            'status': 'PENDING',
            'created_by': admin,
        }
    )
    
    if created:
        wh1 = warehouses['Kho TPHCM (Tân Phú)']
        wh3 = warehouses['Kho Hà Nội (Thanh Xuân)']
        
        OrderTracking.objects.create(
            order=order3,
            warehouse=wh1,
            sequence=1,
            status='PENDING',
        )
        
        OrderTracking.objects.create(
            order=order3,
            warehouse=wh3,
            sequence=2,
            status='PENDING',
        )
        
        print(f"  ✓ Tạo mới: {order3.code} - TPHCM → Hà Nội (Chờ xử lý)")

    # ============================================================================
    # 6. CREATE SINGLE ORDERS
    # ============================================================================
    print("\n📦 Tạo đơn lẻ mẫu...")
    single_orders_data = [
        {
            'code': 'SO-2026-1001',
            'user': drivers['driver001'],
            'customer_name': 'Nguyễn Thị Mai',
            'customer_phone': '0904555666',
            'pickup_point': '123 Nguyễn Văn Cừ, TPHCM',
            'delivery_point': '456 Trần Phú, Quận 5, TPHCM',
            'distance': 4.5,
            'price': 45000,
            'service_type': 'SUPER_FAST',
            'status': 'PENDING',
        },
        {
            'code': 'SO-2026-1002',
            'user': drivers['driver002'],
            'customer_name': 'Công ty Minh Long',
            'customer_phone': '0912333444',
            'pickup_point': '789 Lê Lợi, Quận 1, TPHCM',
            'delivery_point': '1011 Lê Văn Sỹ, Quận 3, TPHCM',
            'distance': 6.2,
            'price': 62000,
            'service_type': '2H',
            'status': 'APPROVED',
        },
        {
            'code': 'SO-2026-1003',
            'user': drivers['driver003'],
            'customer_name': 'Anh Phạm Văn Dũng',
            'customer_phone': '0933777888',
            'pickup_point': '222 Hoàng Hoa Thám, Hà Nội',
            'delivery_point': '333 Phố Huế, Hà Nội',
            'distance': 7.8,
            'price': 78000,
            'service_type': 'SUPER_FAST_ECONOMY',
            'status': 'IN_PROGRESS',
        },
        {
            'code': 'SO-2026-1004',
            'user': drivers['driver004'],
            'customer_name': 'Cửa hàng Hoa Sen',
            'customer_phone': '0943999000',
            'pickup_point': '12 Trần Phú, Hải Dương',
            'delivery_point': '55 Lê Thanh Nghị, Hải Dương',
            'distance': 3.0,
            'price': 30000,
            'service_type': '4H',
            'status': 'DELIVERED',
        },
    ]

    for so_data in single_orders_data:
        single_order, created = SingleOrder.objects.get_or_create(
            code=so_data['code'],
            defaults=so_data
        )
        status = "✓ Tạo mới" if created else "✓ Đã tồn tại"
        print(f"  {status}: {single_order.code} - {single_order.customer_name}")

    print("\n✅ Dữ liệu mẫu tạo thành công!\n")
    print("📊 THỐNG KÊ:")
    print(f"  • Kho bãi: {Warehouse.objects.count()} cái")
    print(f"  • Tài xế: {User.objects.filter(role='DRIVER').count()} người")
    print(f"  • Phương tiện: {Vehicle.objects.count()} chiếc")
    print(f"  • Đơn hàng: {Order.objects.count()} đơn")
    print(f"  • Tracking: {OrderTracking.objects.count()} tracking")
    print("\n🔐 Tài Khoản Đăng Nhập:")
    print("  Admin:")
    print("    • Username: admin123")
    print("    • Password: admin123")
    print("\n  Driver 1:")
    print("    • Username: driver001")
    print("    • Password: driver123")
    print("\n🌐 URL Dashboard:")
    print("  • http://localhost:8000/admin-dashboard/")

if __name__ == '__main__':
    create_sample_data()