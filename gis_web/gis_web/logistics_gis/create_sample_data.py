from core.models import Warehouse, Vehicle

def create_sample_data():
    # Create warehouses
    Warehouse.objects.get_or_create(
        name='Warehouse 1',
        defaults={'lat': 10.762622, 'lng': 106.660172}
    )
    Warehouse.objects.get_or_create(
        name='Warehouse 2',
        defaults={'lat': 10.752622, 'lng': 106.650172}
    )

    # Create vehicles
    Vehicle.objects.get_or_create(
        name='Vehicle 1',
        defaults={
            'driver_name': 'Nguyễn Văn A',
            'driver_birth_year': 1988,
            'plate_number': '51A-12345',
            'vehicle_type': 'Xe tải nhỏ',
            'lat': 10.772622,
            'lng': 106.670172,
            'status': 'ACTIVE',
        }
    )
    Vehicle.objects.get_or_create(
        name='Vehicle 2',
        defaults={
            'driver_name': 'Trần Thị B',
            'driver_birth_year': 1990,
            'plate_number': '51B-54321',
            'vehicle_type': 'Xe Van',
            'lat': 10.742622,
            'lng': 106.640172,
            'status': 'ACTIVE',
        }
    )

    print("Sample data created successfully!")

if __name__ == '__main__':
    create_sample_data()