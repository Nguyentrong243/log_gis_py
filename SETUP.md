# Hướng Dẫn Cài Đặt Hệ Thống Logistics GIS

## 1. CHUẨN BỊ MÔI TRƯỜNG

### 1.1 Cài đặt Python & Dependencies
```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### 1.2 Cấu hình Email (Gmail/Mailtrap)

#### Option A: Sử dụng Gmail
1. Vào [Google Account Settings](https://myaccount.google.com/)
2. Chọn "Security" → "App passwords"
3. Tạo app password cho Django
4. Cập nhật `settings.py`:
```python
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
```

#### Option B: Sử dụng Mailtrap
1. Đăng ký tại [Mailtrap.io](https://mailtrap.io/)
2. Lấy SMTP credentials
3. Cập nhật `settings.py`:
```python
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_HOST_USER = 'your_mailtrap_user'
EMAIL_HOST_PASSWORD = 'your_mailtrap_password'
```

### 1.3 Cấu hình reCAPTCHA (Google reCAPTCHA v3)
1. Vào [Google reCAPTCHA Admin Console](https://www.google.com/recaptcha/admin)
2. Tạo key mới
3. Cập nhật `settings.py`:
```python
RECAPTCHA_SITE_KEY = 'your_site_key'
RECAPTCHA_SECRET_KEY = 'your_secret_key'
```

## 2. THIẾT LẬP CƠ SỐ DỮ LIỆU

```bash
# Tạo migrations
python manage.py makemigrations

# Áp dụng migrations
python manage.py migrate

# Tạo superuser (admin)
python manage.py createsuperuser

# Tên: admin
# Email: admin@logisticsgis.com
# Password: admin123
```

## 3. TẠO DỮ LIỆU BAN ĐẦU

```bash
# Tạo các bảng giá mẫu
python manage.py shell
>>> from core.models import PriceList
>>> # Tạo bảng giá STANDARD
>>> PriceList.objects.create(
...     order_type='STANDARD',
...     distance_from=0,
...     distance_to=10,
...     base_price=30000,
...     per_km_price=5000
... )
>>> PriceList.objects.create(
...     order_type='STANDARD',
...     distance_from=10,
...     distance_to=30,
...     base_price=50000,
...     per_km_price=4000
... )
>>> PriceList.objects.create(
...     order_type='EXPRESS',
...     distance_from=0,
...     distance_to=10,
...     base_price=50000,
...     per_km_price=7000
... )
>>> exit()
```

## 4. CHẠY SERVER

```bash
# Chạy development server
python manage.py runserver

# Truy cập:
# Admin: http://localhost:8000/admin
# Home: http://localhost:8000/
# API: http://localhost:8000/api/
```

## 5. CẤUTRÚC DỰ ÁN

```
logistics_gis/
├── manage.py
├── requirements.txt
├── db.sqlite3
├── media/                    # Thư mục upload file
│   ├── news/
│   └── cv/
├── static/                   # CSS, JS, hình ảnh tĩnh
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── map.js           # GIS map integration
│       └── map_page.js
├── templates/
│   ├── base.html
│   ├── core/
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── register.html
│   │   └── map.html         # Order creation with GIS
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── order_management.html
│   │   └── warehouse_tracking.html
│   ├── user/
│   │   ├── dashboard.html
│   │   ├── create_order.html
│   │   └── track_order.html
│   ├── news/
│   │   ├── list.html
│   │   └── detail.html
│   └── recruitment/
│       ├── list.html
│       ├── detail.html
│       └── apply.html
├── logistics_gis/           # Project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── core/                    # Main app
    ├── models.py            # Models (User, Order, Warehouse, ...)
    ├── admin.py             # Django admin configuration
    ├── views.py             # Views
    ├── urls.py              # URL routing
    ├── forms.py             # Django forms
    ├── services.py          # Business logic (GIS, Pricing, Tracking)
    ├── api_views.py         # REST API views
    ├── serializers.py       # DRF serializers
    ├── management/
    │   └── commands/        # Custom Django commands
    ├── migrations/          # Database migrations
    └── tests.py             # Unit tests
```

## 6. DATABASE SCHEMA (ERD)

### Mối Quan Hệ:
- User (1) -> (N) Order
- User (1) -> (N) Vehicle (tài xế)
- Order (1) -> (N) OrderTracking
- OrderTracking (N) -> (1) Warehouse
- Order (1) -> (1) Promotion (khuyến mãi)
- Order (1) -> (N) OrderTrackingLog
- Recruitment (1) -> (N) JobApplication
- User (1) -> (N) UserDiscount

### Main Models:

**User**
- id, username, email, password
- phone_number, id_card_number, date_of_birth
- address, ward, district, city
- role (USER, ADMIN, DRIVER)
- email_verified, email_verified_at
- profile_completed

**Order**
- id, code (tự động: LOG-YYYY-XXXX)
- customer_name, customer_phone, customer_address
- pickup_point, pickup_lat/lng
- delivery_point, delivery_lat/lng
- recipient_name, recipient_phone
- distance_km, route_polyline
- base_price, additional_price, discount_amount, total_price
- product_type, product_size, order_type
- status (PENDING, APPROVED, IN_PROGRESS, DELIVERED, CANCELLED)
- payment_status (PAID, UNPAID)
- assigned_vehicle, driver_name
- created_by (FK User), created_at, updated_at

**OrderTracking** (Multi-warehouse)
- id, order (FK), warehouse (FK)
- sequence (thứ tự kho)
- status (PENDING, CHECKED_IN, IN_TRANSIT, DELIVERED)
- checked_in_at, checked_in_by (FK User)
- notes

**OrderTrackingLog** (Sync data real-time)
- id (UUID), order (FK), warehouse (FK)
- action (CHECK_IN, IN_TRANSIT, DELIVERED, CANCELLED)
- user (FK User), notes
- created_at

**Warehouse**
- id, name, address
- manager_name, manager_phone
- lat, lng
- created_at, updated_at

**Vehicle**
- id, name, plate_number, vehicle_type
- driver_name, driver_birth_year
- lat, lng, status

**PriceList**
- id, order_type (STANDARD, EXPRESS, BULK)
- distance_from, distance_to
- base_price, per_km_price

**Promotion**
- id, code (unique)
- description
- discount_type (PERCENTAGE, FIXED)
- discount_value
- min_order_amount
- max_usage, usage_count
- is_active
- start_date, end_date

**UserDiscount**
- id, user (FK), promotion (FK)
- granted_at, is_used, used_at
- used_in_order (FK Order)

**News**
- id, title, slug (unique)
- content, featured_image
- author (FK User)
- is_published, published_at
- created_at, updated_at

**Recruitment**
- id, position, slug (unique)
- description, requirements
- salary_from, salary_to
- is_active
- created_at, updated_at

**JobApplication**
- id, recruitment (FK)
- applicant_name, applicant_email, applicant_phone
- cv_file, cover_letter
- status (PENDING, REVIEWED, REJECTED, ACCEPTED)
- reviewed_by (FK User), reviewed_at
- notes
- created_at

## 7. API ENDPOINTS

### Authentication
- POST `/api-auth/login/` - Đăng nhập
- POST `/api-auth/logout/` - Đăng xuất

### Orders
- GET/POST `/api/orders/` - Danh sách/Tạo đơn
- GET `/api/orders/{id}/` - Chi tiết đơn
- POST `/api/orders/{id}/calculate-price/` - Tính giá
- GET `/api/orders/{id}/track/` - Tracking info
- POST `/api/orders/suggest-route/` - Gợi ý route

### Vehicles
- GET `/api/vehicles/` - Danh sách phương tiện
- GET `/api/vehicles/available/` - Phương tiện khả dụng

### Warehouses
- GET `/api/warehouses/` - Danh sách kho
- GET `/api/warehouses/nearby/` - Kho gần nhất (lat, lng, radius)

### Order Tracking
- GET/POST `/api/order-trackings/` - Danh sách tracking
- POST `/api/order-trackings/{id}/check-in/` - Check-in kho

### News
- GET `/api/news/` - Danh sách tin tức

### Recruitment
- GET `/api/recruitment/` - Danh sách tuyển dụng
- GET/POST `/api/job-applications/` - Hồ sơ ứng tuyển

### Promotions
- POST `/api/promotions/validate/` - Kiểm tra mã giảm giá

## 8. FEATURES ĐÃ TRIỂN KHAI

### ✅ Module Quản Lý Tài Xế & Phương Tiện
- [x] Dashboard quản lý phương tiện (Tên, CCCD, Biển số)
- [x] Thông tin tài xế gắn với phương tiện
- [x] Quản lý không giới hạn đối tác/phương tiện
- [x] Model Vehicle mở rộng

### ✅ Module Quản Lý Kho & Đơn Hàng Đa Điểm
- [x] Thông tin kho: Tên, Vị trí GIS, Quản lý kho
- [x] OrderTracking multi-warehouse
- [x] Check-in điểm danh tại kho
- [x] OrderTrackingLog sync data real-time

### ✅ Module Người Dùng & Đặt Đơn Hàng
- [x] Tự động sinh mã đơn (LOG-2026-XXXX)
- [x] Tích hợp GIS: pickup/delivery points
- [x] Tính khoảng cách Haversine
- [x] Bảng giá dựa trên khoảng cách
- [x] Tính phí tự động

### ✅ Module Tin Tức, Khuyến Mãi & Tuyển Dụng
- [x] CRUD tin tức (với hình ảnh)
- [x] Trang Tuyển dụng public
- [x] Quản lý hồ sơ ứng tuyển
- [x] Hệ thống khuyến mãi/mã giảm giá
- [x] Tự động cấp mã giảm cho user

### ✅ Cấu Hình Cơ Bản
- [x] Settings.py mở rộng (Email, Media, CAPTCHA)
- [x] Requirements.txt đầy đủ
- [x] Models toàn diện
- [x] Admin interface customized
- [x] Forms validation

## 9. TIẾP THEO CẦN LÀM

### Views & Templates
- [ ] Django views cho từng trang
- [ ] HTML templates responsive
- [ ] Bootstrap 5 integration

### GIS JavaScript
- [ ] Leaflet.js tích hợp
- [ ] Vẽ tuyến đường
- [ ] Real-time tracking map

### Email & OTP
- [ ] Email confirmation
- [ ] OTP verification
- [ ] reCAPTCHA integration

### Management Commands
- [ ] Tạo test data
- [ ] Init bảng giá
- [ ] Cleanup jobs

## 10. TESTING

```bash
# Chạy tests
python manage.py test

# Chạy tests với coverage
coverage run --source='.' manage.py test
coverage report
```

## 11. DEPLOYMENT

### Production Checklist
- [ ] DEBUG = False
- [ ] SECRET_KEY đã thay đổi
- [ ] ALLOWED_HOSTS cấu hình
- [ ] HTTPS enabled
- [ ] Database migration
- [ ] Collect staticfiles
- [ ] Email configuration
- [ ] Backup strategy

### Deploying to Heroku/PythonAnywhere
```bash
# Heroku
heroku create
heroku config:set DEBUG=False
git push heroku main

# PythonAnywhere
# Upload files via SFTP
# Configure WSGI
# Reload app
```

## 12. LIÊN HỆ & HỖ TRỢ

- Documentation: Xem comments trong code
- Issues: Sử dụng Django debug toolbar
- Logs: `logs/` folder

---

**Phiên bản**: 1.0.0  
**Cập nhật lần cuối**: 2026-04-20  
**Tác giả**: Logistics GIS Team
