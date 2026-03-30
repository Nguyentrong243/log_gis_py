from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    ROLE_CHOICES = [
        ('USER', 'User'),
        ('ADMIN', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')

    def __str__(self):
        return self.username

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('IN_PROGRESS', 'In progress'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    PRODUCT_SIZE_CHOICES = [
        ('SMALL', 'Nhỏ (S)'),
        ('MEDIUM', 'Vừa (M)'),
        ('LARGE', 'To (L)'),
    ]
    
    PRODUCT_TYPE_CHOICES = [
        ('FASHION', 'Thời Trang'),
        ('COSMETICS', 'Mĩ Phẩm'),
        ('ELECTRONICS', 'Điện Tử'),
        ('HOUSEHOLD', 'Gia Dụng'),
        ('FOOD', 'Thực Phẩm'),
        ('OTHER', 'Khác'),
    ]
    
    code = models.CharField(max_length=10, unique=True)
    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15, blank=True, null=True)
    order_type = models.CharField(max_length=50, default='Standard')
    lat = models.FloatField()
    lng = models.FloatField()
    customer_address = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='PENDING')
    assigned_vehicle = models.ForeignKey('Vehicle', null=True, blank=True, on_delete=models.SET_NULL)
    estimated_eta = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # New fields for delivery details
    pickup_point = models.CharField(max_length=255, blank=True, null=True, verbose_name='Điểm nhận hàng')
    delivery_point = models.CharField(max_length=255, blank=True, null=True, verbose_name='Điểm giao hàng')
    
    # Driver info
    driver_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Tên tài xế')
    driver_address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Địa chỉ tài xế')
    
    # Product information
    product_size = models.CharField(max_length=20, choices=PRODUCT_SIZE_CHOICES, blank=True, null=True, verbose_name='Kích cỡ hàng')
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPE_CHOICES, blank=True, null=True, verbose_name='Loại hàng hóa')
    
    # Recipient information
    recipient_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Tên người nhận')
    recipient_phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Số điện thoại người nhận')
    
    # Payment information
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Giá tiền')
    payment_status = models.CharField(max_length=20, choices=[('UNPAID', 'Chưa thanh toán'), ('PAID', 'Đã thanh toán')], default='UNPAID', verbose_name='Trạng thái thanh toán')
    
    # Cancellation information
    driver_cancel_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Tên tài xế hủy chuyến')
    driver_cancel_phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Số điện thoại tài xế hủy')
    cancel_reason = models.TextField(blank=True, null=True, verbose_name='Lý do hủy chuyến')
    cancelled_at = models.DateTimeField(blank=True, null=True, verbose_name='Thời gian hủy')

    def __str__(self):
        return f"{self.code} - {self.customer_name}"

class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('ON_DELIVERY', 'On delivery'),
    ]
    name = models.CharField(max_length=100)
    driver_name = models.CharField(max_length=100, blank=True, null=True)
    driver_birth_year = models.PositiveIntegerField(blank=True, null=True)
    plate_number = models.CharField(max_length=20, blank=True, null=True)
    vehicle_type = models.CharField(max_length=50, blank=True, null=True)
    lat = models.FloatField()
    lng = models.FloatField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ACTIVE')

    def __str__(self):
        return f"{self.name} ({self.plate_number if self.plate_number else 'no plate'})"
    
    def get_current_orders(self):
        """Get all current orders assigned to this vehicle"""
        return self.order_set.filter(status__in=['APPROVED', 'IN_PROGRESS']).order_by('created_at')

class Warehouse(models.Model):
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()

    def __str__(self):
        return self.name
