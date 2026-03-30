from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView, UpdateView
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from .models import Order, Vehicle, Warehouse
from .forms import CustomUserCreationForm, OrderForm, AdminOrderManagementForm
from django.http import JsonResponse
from django.core.mail import send_mail
import json
import math
from functools import wraps
from django.views.decorators.csrf import csrf_exempt

def is_admin_user(user):
    return user.is_authenticated and (user.is_superuser or user.role == 'ADMIN')


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login first.')
            return redirect('login')
        if not is_admin_user(request.user):
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def home(request):
    return render(request, 'core/home.html')

def ship_now(request):
    if request.user.is_authenticated:
        if is_admin_user(request.user):
            return redirect('admin_dashboard')
        return redirect('map')
    return redirect('login')

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'core/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        send_mail(
            'Welcome to Logistics GIS',
            'Your account has been created successfully.',
            'noreply@logisticsgis.com',
            [user.email],
            fail_silently=False,
        )
        messages.success(self.request, 'Registration successful. Please log in now.')
        return redirect(self.success_url)

class CustomLoginView(LoginView):
    template_name = 'core/login.html'

    def get_success_url(self):
        # Sau khi login, admin và user đều đến trang map toàn cầu
        return reverse_lazy('map')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')

@login_required
def dashboard(request):
    if is_admin_user(request.user):
        return redirect('admin_dashboard')
    return redirect('map')
    if is_admin_user(request.user):
        orders = Order.objects.all()
        template = 'core/admin/dashboard.html'
    else:
        orders = Order.objects.filter(created_by=request.user)
        template = 'core/user/dashboard.html'
    vehicles = Vehicle.objects.all()
    warehouses = Warehouse.objects.all()
    pending_count = orders.filter(status='PENDING').count()
    approved_count = orders.filter(status='APPROVED').count()
    return render(request, template, {
        'orders': orders,
        'vehicles': vehicles,
        'warehouses': warehouses,
        'pending_count': pending_count,
        'approved_count': approved_count,
    })

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = form.save(commit=False)
                order.created_by = request.user
                order.status = 'PENDING'
                order.estimated_eta = 'Đang chờ admin duyệt'
                
                # Generate sequential code based on Vietnam time
                # Find the next available code
                last_order = Order.objects.select_for_update().order_by('-created_at').first()
                start_num = 1
                if last_order and last_order.code:
                    try:
                        last_num = int(last_order.code.replace('ĐH', ''))
                        start_num = last_num + 1
                    except:
                        start_num = 1
                
                # Ensure uniqueness
                while Order.objects.filter(code=f'ĐH{start_num:03d}').exists():
                    start_num += 1
                
                order.code = f'ĐH{start_num:03d}'
                
                order.save()
                messages.success(request, f'✓ Đặt đơn thành công! Mã: {order.code}')
                return redirect('map')
    else:
        form = OrderForm()
    return render(request, 'core/user/create_order.html', {'form': form})

@admin_required
def approve_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # 1) Tìm kho gần nhất với đơn hàng
    warehouses = Warehouse.objects.all()
    nearest_warehouse = None
    shortest_wh_dist = None
    for warehouse in warehouses:
        dist_wh = haversine(order.lat, order.lng, warehouse.lat, warehouse.lng)
        if shortest_wh_dist is None or dist_wh < shortest_wh_dist:
            shortest_wh_dist = dist_wh
            nearest_warehouse = warehouse

    # 2) Tìm tài xế rảnh (ACTIVE, không có ĐƠN IN_PROGRESS hoặc APPROVED) và gần kho nhất
    busy_vehicles = Vehicle.objects.filter(order__status__in=['APPROVED', 'IN_PROGRESS']).values_list('id', flat=True)
    available_vehicles = Vehicle.objects.filter(status='ACTIVE').exclude(id__in=busy_vehicles)

    assigned_vehicle = None
    shortest_drv_dist = None
    if nearest_warehouse:
        for vehicle in available_vehicles:
            drv_dist = haversine(nearest_warehouse.lat, nearest_warehouse.lng, vehicle.lat, vehicle.lng)
            if shortest_drv_dist is None or drv_dist < shortest_drv_dist:
                shortest_drv_dist = drv_dist
                assigned_vehicle = vehicle

    # 3) Cập nhật đơn hàng và gán tài xế / kho nếu có
    order.status = 'IN_PROGRESS' if assigned_vehicle else 'APPROVED'
    order.estimated_eta = '15-20 phút'
    if assigned_vehicle:
        order.assigned_vehicle = assigned_vehicle
    if nearest_warehouse:
        order.pickup_point = nearest_warehouse.name
    order.save()

    messages.success(request, 'Order approved and assigned to driver.' if assigned_vehicle else 'Order approved (no available driver).')
    return redirect('admin_dashboard')

@csrf_exempt
def api_orders(request):
    try:
        orders = Order.objects.filter(status__in=['APPROVED', 'IN_PROGRESS'])
        result = []
        for order in orders:
            route = None
            if order.assigned_vehicle and order.pickup_point:
                warehouse = Warehouse.objects.filter(name=order.pickup_point).first()
                if warehouse:
                    route = [
                        {'name': warehouse.name, 'lat': warehouse.lat, 'lng': warehouse.lng},
                        {'name': 'Customer', 'lat': order.lat, 'lng': order.lng}
                    ]

            result.append({
                'code': order.code,
                'customer_name': order.customer_name,
                'customer_address': order.customer_address,
                'lat': order.lat,
                'lng': order.lng,
                'status': order.status,
                'estimated_eta': order.estimated_eta,
                'assigned_vehicle_name': order.assigned_vehicle.name if order.assigned_vehicle else None,
                'assigned_vehicle_plate': order.assigned_vehicle.plate_number if order.assigned_vehicle else None,
                'assigned_vehicle_driver': order.assigned_vehicle.driver_name if order.assigned_vehicle else None,
                'pickup_point': order.pickup_point,
                'route': route,
            })

        return JsonResponse(result, safe=False)
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)

@csrf_exempt
def api_vehicles(request):
    try:
        vehicles = Vehicle.objects.all().values('name', 'driver_name', 'driver_birth_year', 'plate_number', 'vehicle_type', 'lat', 'lng', 'status')
        return JsonResponse(list(vehicles), safe=False)
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)

@csrf_exempt
def api_warehouses(request):
    try:
        warehouses = Warehouse.objects.all().values('name', 'lat', 'lng')
        return JsonResponse(list(warehouses), safe=False)
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)

@login_required
def api_map_data(request):
    try:
        orders = Order.objects.filter(status__in=['APPROVED', 'IN_PROGRESS', 'PENDING'])
        order_list = []
        for order in orders:
            route = None
            if order.assigned_vehicle and order.pickup_point:
                warehouse = Warehouse.objects.filter(name=order.pickup_point).first()
                if warehouse:
                    route = [
                        {'name': warehouse.name, 'lat': warehouse.lat, 'lng': warehouse.lng},
                        {'name': 'Customer', 'lat': order.lat, 'lng': order.lng}
                    ]

            order_list.append({
                'code': order.code,
                'customer_name': order.customer_name,
                'customer_address': order.customer_address,
                'lat': order.lat,
                'lng': order.lng,
                'status': order.status,
                'estimated_eta': order.estimated_eta,
                'assigned_vehicle_name': order.assigned_vehicle.name if order.assigned_vehicle else None,
                'assigned_vehicle_plate': order.assigned_vehicle.plate_number if order.assigned_vehicle else None,
                'assigned_vehicle_driver': order.assigned_vehicle.driver_name if order.assigned_vehicle else None,
                'pickup_point': order.pickup_point,
                'route': route,
            })

        return JsonResponse({
            'warehouses': list(Warehouse.objects.all().values('name', 'lat', 'lng')),
            'vehicles': list(Vehicle.objects.all().values('name', 'driver_name', 'driver_birth_year', 'plate_number', 'vehicle_type', 'lat', 'lng', 'status')),
            'orders': order_list,
        })
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)

@login_required
def map_view(request):
    if request.method == 'POST':
        with transaction.atomic():
            # Auto-generate sequential code: ĐH001, ĐH002, etc.
            last_order = Order.objects.select_for_update().order_by('-created_at').first()
            start_num = 1
            if last_order and last_order.code:
                try:
                    last_num = int(last_order.code.replace('ĐH', ''))
                    start_num = last_num + 1
                except:
                    start_num = 1
            
            # Ensure uniqueness
            while Order.objects.filter(code=f'ĐH{start_num:03d}').exists():
                start_num += 1
            
            code = f'ĐH{start_num:03d}'
            
            Order.objects.create(
                code=code,
            customer_name=request.POST.get('customer_name'),
            customer_phone=request.POST.get('customer_phone'),
            lat=request.POST.get('lat'),
            lng=request.POST.get('lng'),
            created_by=request.user,
            status='PENDING',
            delivery_point=request.POST.get('delivery_point'),
            recipient_name=request.POST.get('recipient_name'),
            recipient_phone=request.POST.get('recipient_phone'),
            product_type=request.POST.get('product_type'),
            customer_address=request.POST.get('customer_address'),
        )
        return redirect('map')

    return render(request, 'core/map.html')

@admin_required
def admin_dashboard(request):
    """Enhanced admin dashboard with filtering and statistics"""
    # Get all orders sorted by creation time (oldest first = first to be reviewed)
    orders = Order.objects.all().order_by('created_at')
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')
    
    # Apply filters
    if status_filter != 'all' and status_filter:
        orders = orders.filter(status=status_filter)
    
    if search_query:
        orders = orders.filter(
            code__icontains=search_query
        ) | orders.filter(
            customer_name__icontains=search_query
        ) | orders.filter(
            customer_phone__icontains=search_query
        )
    
    # Get vehicles and warehouses
    vehicles = Vehicle.objects.all()
    warehouses = Warehouse.objects.all()
    
    # Calculate statistics
    all_orders = Order.objects.all()
    pending_count = all_orders.filter(status='PENDING').count()
    approved_count = all_orders.filter(status='APPROVED').count()
    in_progress_count = all_orders.filter(status='IN_PROGRESS').count()
    delivered_count = all_orders.filter(status='DELIVERED').count()
    cancelled_count = all_orders.filter(status='CANCELLED').count()
    total_orders = all_orders.count()
    
    # Calculate revenue
    total_revenue = all_orders.aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    return render(request, 'core/admin/dashboard.html', {
        'orders': orders,
        'vehicles': vehicles,
        'warehouses': warehouses,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'in_progress_count': in_progress_count,
        'delivered_count': delivered_count,
        'cancelled_count': cancelled_count,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'status_filter': status_filter,
        'search_query': search_query,
    })

@admin_required
def admin_order_management(request):
    """Admin view to manage orders with all details"""
    if request.method == 'POST':
        form = AdminOrderManagementForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.status = form.cleaned_data.get('status', 'PENDING')
            order.save()
            messages.success(request, 'Đơn hàng đã được lưu thành công!')
            return redirect('admin_dashboard')
    else:
        form = AdminOrderManagementForm()
    
    return render(request, 'core/admin/order_management.html', {
        'form': form
    })

@admin_required
def admin_edit_order(request, order_id):
    """Admin view to edit existing orders"""
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        form = AdminOrderManagementForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đơn hàng đã được cập nhật thành công!')
            return redirect('admin_dashboard')
    else:
        form = AdminOrderManagementForm(instance=order)
    
    return render(request, 'core/admin/order_management.html', {
        'form': form,
        'order': order
    })
@admin_required
def cancel_order(request):
    """Cancel an order with cancellation reason and driver information"""
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        driver_name = request.POST.get('driver_name')
        driver_phone = request.POST.get('driver_phone')
        cancel_reason = request.POST.get('cancel_reason')
        
        try:
            order = get_object_or_404(Order, id=order_id)
            
            # Store cancellation information in the order
            order.status = 'CANCELLED'
            order.driver_cancel_name = driver_name
            order.driver_cancel_phone = driver_phone
            order.cancel_reason = cancel_reason
            order.cancelled_at = timezone.now()
            order.save()
            
            return JsonResponse({'success': True, 'message': 'Đơn hàng đã được hủy thành công'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_vehicle_orders(request, vehicle_id):
    """Get all orders assigned to a vehicle"""
    try:
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        orders = vehicle.get_current_orders()
        
        data = {
            'vehicle_id': vehicle.id,
            'driver_name': vehicle.driver_name,
            'orders': list(orders.values('id', 'code', 'customer_name', 'customer_address', 'status'))
        }
        return JsonResponse(data)
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)