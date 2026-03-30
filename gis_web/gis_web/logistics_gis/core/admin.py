from django.contrib import admin
from .models import Order, Vehicle, Warehouse, User

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('code', 'customer_name', 'status', 'total_price', 'created_at', 'cancelled_at')
    list_filter = ('status', 'created_at', 'cancelled_at')
    search_fields = ('code', 'customer_name', 'customer_phone')
    readonly_fields = ('code', 'created_at', 'cancelled_at')
    fieldsets = (
        ('Thông tin đơn hàng', {
            'fields': ('code', 'customer_name', 'customer_phone', 'customer_address', 'status', 'created_at', 'created_by')
        }),
        ('Giao hàng', {
            'fields': ('delivery_point', 'recipient_name', 'recipient_phone', 'assigned_vehicle', 'estimated_eta')
        }),
        ('Sản phẩm', {
            'fields': ('product_type', 'product_size', 'total_price', 'payment_status')
        }),
        ('Vị trí', {
            'fields': ('lat', 'lng')
        }),
        ('Hủy chuyến', {
            'fields': ('driver_cancel_name', 'driver_cancel_phone', 'cancel_reason', 'cancelled_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'driver_name', 'plate_number', 'status', 'vehicle_type')
    list_filter = ('status', 'vehicle_type')
    search_fields = ('name', 'driver_name', 'plate_number')

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'lat', 'lng')
    search_fields = ('name',)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff')
    search_fields = ('username', 'email')
