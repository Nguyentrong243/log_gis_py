from django.core.management.base import BaseCommand
from core.models import Warehouse
import random

class Command(BaseCommand):
    help = 'Create 20 sample warehouses with random locations across Vietnam land territory'

    def handle(self, *args, **options):
        # Safe inland locations in Vietnam (avoiding coastal areas)
        safe_locations = [
            # Hà Nội area
            (21.0285, 105.8542),  # Hà Nội center
            (21.0165, 105.8428),  # Ba Đình
            (20.9860, 105.8476),  # Từ Liêm
            
            # TP.HCM area
            (10.7769, 106.6966),  # District 1
            (10.7588, 106.6758),  # District 3
            (10.7282, 106.6537),  # District 5
            (10.8065, 106.6651),  # Tân Bình
            
            # Other inland cities
            (16.0544, 108.2022),  # Đà Nẵng (inland part)
            (10.0364, 105.7867),  # Cần Thơ
            (12.2388, 109.1967),  # Nha Trang (inland)
            (18.6889, 105.6942),  # Vinh
            (13.7778, 109.2264),  # Quy Nhơn
            (10.8968, 106.7640),  # Bình Dương
            (11.0413, 107.0637),  # Đồng Nai
            (10.3708, 106.3669),  # Tiền Giang
            (20.9550, 107.0371),  # Hạ Long (inland)
            (15.8794, 108.3350),  # Tam Kỳ
            (11.9280, 109.1500),  # Phan Rang
            (9.1769, 105.1500),   # Rạch Giá
            (10.3450, 105.4500),  # Sa Đéc
            (11.3000, 106.1000),  # Tây Ninh
            (11.5500, 106.6500),  # Bình Phước
            (12.7000, 108.0500),  # Đắk Lắk
            (13.9833, 108.0000),  # Kon Tum
            (14.3500, 107.9833),  # Gia Lai
            (16.4667, 107.6000),  # Quảng Nam
            (17.4833, 106.6000),  # Quảng Bình
            (19.8000, 105.7833),  # Thanh Hóa
            (20.4167, 106.1667),  # Thái Bình
            (20.9500, 106.3333),  # Hải Dương
            (21.3167, 106.0833),  # Bắc Giang
            (21.3833, 105.3667),  # Phú Thọ
            (21.8167, 105.2167),  # Yên Bái
            (22.1333, 104.8333),  # Lào Cai
            (22.6667, 106.2500),  # Cao Bằng
            (22.8333, 106.6667),  # Lạng Sơn
        ]

        # Create 20 warehouses
        warehouses = []
        for i in range(20):
            code = f"KH{i+1:03d}"  # KH001, KH002, etc.
            name = f"Kho {code}"
            
            # Choose a random safe location
            lat, lng = random.choice(safe_locations)
            # Add small variation
            lat += random.uniform(-0.01, 0.01)
            lng += random.uniform(-0.01, 0.01)
            
            warehouse, created = Warehouse.objects.get_or_create(
                name=name,
                defaults={'lat': lat, 'lng': lng}
            )
            if created:
                warehouses.append(warehouse)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(warehouses)} warehouses with codes KH001 to KH020')
        )