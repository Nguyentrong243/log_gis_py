from django.contrib import admin
from .models import Warehouse, Order, Vehicle

admin.site.register(Warehouse)
admin.site.register(Order)
admin.site.register(Vehicle)