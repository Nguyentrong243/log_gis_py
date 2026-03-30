from django.core.management.base import BaseCommand
from core.models import Vehicle
import random

class Command(BaseCommand):
    help = 'Update all vehicle locations to safe inland coordinates in Vietnam'

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
        ]

        vehicles = Vehicle.objects.all()
        updated_count = 0
        
        for vehicle in vehicles:
            # Choose a random safe location
            lat, lng = random.choice(safe_locations)
            # Add small variation to avoid exact same locations
            vehicle.lat = lat + random.uniform(-0.005, 0.005)
            vehicle.lng = lng + random.uniform(-0.005, 0.005)
            vehicle.save()
            updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} vehicles to safe inland locations in Vietnam')
        )