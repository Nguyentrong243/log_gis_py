from django.shortcuts import render
from .models import Warehouse, Order, Vehicle

def map_view(request):
    warehouses = Warehouse.objects.all()
    orders = Order.objects.all()
    vehicles = Vehicle.objects.all()

    warehouse = warehouses.first()
    vehicle = vehicles.first()  # 👈 thêm dòng này

    return render(request, "map.html", {
        "warehouses": warehouses,
        "orders": orders,
        "vehicles": vehicles,
        "warehouse": warehouse,
        "vehicle": vehicle,  # 👈 truyền qua HTML
    })