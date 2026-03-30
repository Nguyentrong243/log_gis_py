from django.core.management.base import BaseCommand
from core.models import Order, User, Vehicle
import random
import string
from decimal import Decimal

class Command(BaseCommand):
    help = 'Create 10 sample orders with random data'

    def handle(self, *args, **options):
        # Get or create a user
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com', 'role': 'USER'}
        )
        if created:
            user.set_password('password')
            user.save()

        # Vietnamese names
        first_names = ['Nguyễn', 'Trần', 'Phạm', 'Hoàng', 'Huỳnh', 'Võ', 'Phan', 'Lê', 'Dương', 'Thái']
        last_names = ['Văn', 'Thị', 'Quốc', 'Anh', 'Minh', 'Huy', 'Long', 'Khoa', 'Tú', 'Mạnh']

        # Product types
        product_types = ['FASHION', 'COSMETICS', 'ELECTRONICS', 'HOUSEHOLD', 'FOOD', 'OTHER']

        # Get active vehicles locations
        active_vehicles = Vehicle.objects.filter(status='ACTIVE')
        if active_vehicles.exists():
            vehicle_locations = list(active_vehicles.values_list('lat', 'lng'))
        else:
            # Fallback to some default locations if no active vehicles
            vehicle_locations = [
                (10.7769, 106.6966),  # TP.HCM
                (21.0285, 105.8542),  # Hà Nội
            ]

        # Get the last order code to continue sequentially
        last_order = Order.objects.all().order_by('-created_at').first()
        start_num = 1
        if last_order and last_order.code:
            try:
                last_num = int(last_order.code.replace('ĐH', ''))
                start_num = last_num + 1
            except:
                start_num = 1

        orders = []
        for i in range(10):
            # Find next available code
            while True:
                code = f"ĐH{start_num + i:03d}"
                if not Order.objects.filter(code=code).exists():
                    break
                start_num += 1
            
            # Generate names
            customer_first = random.choice(first_names)
            customer_last = random.choice(last_names)
            customer_name = f"{customer_first} {customer_last}"
            
            recipient_first = random.choice(first_names)
            recipient_last = random.choice(last_names)
            recipient_name = f"{recipient_first} {recipient_last}"
            
            # Generate phones
            customer_phone = f"0{random.randint(100000000, 999999999)}"
            recipient_phone = f"0{random.randint(100000000, 999999999)}"
            
            # Random location near active vehicles
            lat, lng = random.choice(vehicle_locations)
            lat += random.uniform(-0.005, 0.005)  # Small variation
            lng += random.uniform(-0.005, 0.005)
            
            # Random addresses
            streets = ['Đường Lê Lợi', 'Đường Nguyễn Huệ', 'Đường Trần Hưng Đạo', 'Đường Phạm Ngũ Lão', 'Đường Cách Mạng Tháng 8']
            customer_address = f"{random.randint(1, 100)} {random.choice(streets)}, Quận {random.randint(1, 12)}, TP.HCM"
            delivery_point = f"{random.randint(1, 100)} {random.choice(streets)}, Quận {random.randint(1, 12)}, TP.HCM"
            
            # Random product type and price
            product_type = random.choice(product_types)
            total_price = Decimal(random.uniform(50000, 500000)).quantize(Decimal('0.01'))
            
            order = Order(
                code=code,
                customer_name=customer_name,
                customer_phone=customer_phone,
                customer_address=customer_address,
                recipient_name=recipient_name,
                recipient_phone=recipient_phone,
                delivery_point=delivery_point,
                product_type=product_type,
                total_price=total_price,
                lat=lat,
                lng=lng,
                created_by=user,
                status='PENDING'
            )
            orders.append(order)

        # Bulk create
        Order.objects.bulk_create(orders)
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created 10 random orders with codes ĐH001 to ĐH010')
        )