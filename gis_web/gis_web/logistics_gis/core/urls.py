from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ship-now/', views.ship_now, name='ship_now'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-order-management/', views.admin_order_management, name='admin_order_management'),
    path('admin-order-edit/<int:order_id>/', views.admin_edit_order, name='admin_edit_order'),
    path('map/', views.map_view, name='map'),
    path('create-order/', views.create_order, name='create_order'),
    path('approve-order/<int:order_id>/', views.approve_order, name='approve_order'),
    path('cancel-order/', views.cancel_order, name='cancel_order'),
    path('api/orders/', views.api_orders, name='api_orders'),
    path('api/vehicles/', views.api_vehicles, name='api_vehicles'),
    path('api/warehouses/', views.api_warehouses, name='api_warehouses'),
    path('api/map-data/', views.api_map_data, name='api_map_data'),
    path('api/vehicle-orders/<int:vehicle_id>/', views.api_vehicle_orders, name='api_vehicle_orders'),
]