from django.contrib import admin
from django.urls import path
from core.views import map_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', map_view),  # 👈 route chính
]