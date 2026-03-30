from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Order

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['code', 'customer_name', 'customer_phone', 'order_type', 'customer_address', 'lat', 'lng', 'recipient_name', 'recipient_phone', 'delivery_point', 'product_type']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'order_type': forms.Select(choices=[('Standard','Standard'),('Express','Express'),('Bulk','Bulk')], attrs={'class':'form-select'}),
            'customer_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Địa chỉ khách hàng (nơi nhận)'}),
            'recipient_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tên người nhận', 'required': False}),
            'recipient_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'SĐT người nhận', 'required': False}),
            'delivery_point': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Địa chỉ giao hàng', 'required': False}),
            'product_type': forms.Select(attrs={'class': 'form-select', 'required': False}),
            'lat': forms.HiddenInput(),
            'lng': forms.HiddenInput(),
        }

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if code:
            if len(code) < 2:
                raise forms.ValidationError('Order code must be at least 2 characters.')
            return code.upper()
        return code

    def clean_customer_name(self):
        customer_name = self.cleaned_data.get('customer_name')
        if not customer_name:
            raise forms.ValidationError('Customer name is required.')
        if len(customer_name) < 2:
            raise forms.ValidationError('Customer name must be at least 2 characters.')
        return customer_name

    def clean_lat(self):
        lat = self.cleaned_data.get('lat')
        if lat is None:
            raise forms.ValidationError('Please select a location on the map.')
        if not (-90 <= lat <= 90):
            raise forms.ValidationError('Invalid latitude.')
        return lat

    def clean_lng(self):
        lng = self.cleaned_data.get('lng')
        if lng is None:
            raise forms.ValidationError('Please select a location on the map.')
        if not (-180 <= lng <= 180):
            raise forms.ValidationError('Invalid longitude.')
        return lng


class AdminOrderManagementForm(forms.ModelForm):
    """Form for admin to manage orders with all details"""
    class Meta:
        model = Order
        fields = [
            'code', 'driver_name', 'driver_address', 'pickup_point', 'delivery_point',
            'product_size', 'product_type', 'recipient_name', 'recipient_phone', 
            'total_price', 'customer_name', 'customer_phone', 'customer_address', 
            'assigned_vehicle', 'order_type', 'status', 'payment_status'
        ]
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mã đơn hàng'
            }),
            'driver_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập tên tài xế'
            }),
            'driver_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nhập địa chỉ tài xế'
            }),
            'pickup_point': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bạn muốn nhận hàng ở đâu - Điểm nhận hàng'
            }),
            'delivery_point': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bạn muốn giao hàng đến đâu - Điểm giao hàng'
            }),
            'product_size': forms.Select(attrs={
                'class': 'form-select'
            }),
            'product_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'recipient_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tên người nhận'
            }),
            'recipient_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Số điện thoại người nhận'
            }),
            'total_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Giá tiền',
                'step': '0.01'
            }),
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tên khách hàng'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Số điện thoại khách hàng'
            }),
            'customer_address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Địa chỉ khách hàng'
            }),
            'assigned_vehicle': forms.Select(attrs={
                'class': 'form-select'
            }),
            'order_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'payment_status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }