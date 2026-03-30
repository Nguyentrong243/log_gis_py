from django.core.management.base import BaseCommand
from core.models import Vehicle
import random
from random import choice, randint, uniform

class Command(BaseCommand):
    help = 'Create 20 sample vehicles with random data across Vietnam'

    def handle(self, *args, **options):
        # Vietnamese names
        first_names = ['Nguyễn', 'Trần', 'Phạm', 'Hoàng', 'Huỳnh', 'Võ', 'Phan', 'Lê', 'Dương', 'Thái']
        last_names = ['Văn', 'Thị', 'Quốc', 'Anh', 'Minh', 'Huy', 'Long', 'Khoa', 'Tú', 'Mạnh', 
                      'Hùng', 'Tuấn', 'Bảo', 'Sơn', 'Dũng', 'Kiệm', 'Hiệp', 'Quân', 'Nhân', 'Phát']

        # Vehicle types
        vehicle_types = ['Xe Tải Con', 'Xe Bán Tải', 'Xe Thùng', 'Xe Máy']

        # License plate patterns
        def generate_plate():
            prefix = choice(['29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40'])
            middle = f"-{choice(['A', 'B', 'C', 'D', 'E'])} "
            numbers = f"{randint(10000, 99999)}"
            return f"{prefix}{middle}{numbers}"

        # Vietnam coordinates (major cities and regions)
        vietnam_locations = [
            # Hà Nội area (Nội thành)
            (21.0285, 105.8542),  # Hà Nội center
            (21.0410, 105.7866),  # Hoàn Kiếm
            (21.0165, 105.8428),  # Ba Đình
            
            # TP.HCM area (Nội thành)
            (10.7769, 106.6966),  # District 1
            (10.7588, 106.6758),  # District 3
            (10.7282, 106.6537),  # District 5
            
            # Hai Phòng
            (20.8449, 106.6881),
            (20.8624, 106.6883),
            
            # Đà Nẵng
            (16.0544, 108.2022),
            (16.0676, 108.2147),
            
            # Cần Thơ
            (10.0364, 105.7867),
            (10.0282, 105.7707),
            
            # Vũng Tàu
            (10.3578, 107.0638),
            
            # Nha Trang
            (12.2388, 109.1967),
            
            # Hạ Long
            (20.9550, 107.0371),
            
            # Vinh
            (18.6889, 105.6942),
            
            # Quy Nhơn
            (13.7778, 109.2264),
            
            # Bình Dương
            (10.8968, 106.7640),
            
            # Đồng Nai
            (11.0413, 107.0637),
            
            # Bà Rịa-Vũng Tàu
            (10.2285, 107.1688),
            
            # Tiền Giang
            (10.3708, 106.3669),
        ]

        # Vehicle statuses
        statuses = ['ACTIVE', 'ON_DELIVERY']

        # Create vehicles
        vehicles = []
        for i in range(20):
            first_name = choice(first_names)
            last_name = choice(last_names)
            driver_name = f"{first_name} {last_name}"
            
            vehicle_type = choice(vehicle_types)
            vehicle_name = f"Xe {vehicle_type} {i+1}"
            
            plate_number = generate_plate()
            lat, lng = choice(vietnam_locations)
            status = choice(statuses)
            
            # Determine speed based on vehicle type and location
            # Nội thành (Hà Nội hoặc TP.HCM) = 50km, khác = tùy loại xe
            if (20.8 < lat < 21.1 and 105.7 < lng < 105.9) or (10.6 < lat < 10.9 and 106.5 < lng < 106.8):
                # Nội thành
                speed = 50
            else:
                # Khác
                if vehicle_type == 'Xe Máy':
                    speed = 60
                else:
                    speed = 70
            
            vehicle = Vehicle(
                name=vehicle_name,
                driver_name=driver_name,
                driver_birth_year=randint(1980, 2000),
                plate_number=plate_number,
                vehicle_type=vehicle_type,
                lat=lat + uniform(-0.01, 0.01),  # Add slight random variation
                lng=lng + uniform(-0.01, 0.01),
                status=status
            )
            vehicles.append(vehicle)

        # Bulk create
        Vehicle.objects.bulk_create(vehicles)
        self.stdout.write(self.style.SUCCESS(f'Successfully created 20 vehicles'))
