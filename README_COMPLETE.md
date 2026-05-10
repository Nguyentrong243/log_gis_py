# Logistics GIS - Hệ Thống Quản Lý Logistics & GIS

Một hệ thống web hiện đại cho quản lý logistics, vận chuyển đa điểm, và tính giá tự động dựa trên GIS.

## 🚀 Tính Năng Chính

### 1. **Tích Hợp Bản Đồ GIS (Leaflet.js + OpenStreetMap)**
- Chọn điểm nhận/giao bằng click trên bản đồ
- Vẽ tuyến đường và tính khoảng cách tự động
- Hiển thị tracking real-time trên bản đồ
- Zoom, pan, marker với phong cách custom

### 2. **Tính Giá Tự Động**
- Dựa trên khoảng cách (Haversine formula)
- Loại dịch vụ (Standard, Express, Bulk)
- Hỗ trợ multiple tier pricing
- Áp dụng mã khuyến mãi % hoặc cố định
- Theo dõi sử dụng mã khuyến mãi

### 3. **Theo Dõi Đơn Hàng Đa Điểm**
- Tự động phân chia tuyến qua multiple warehouses
- Check-in tại từng điểm với audit log
- Timeline trực quan theo status
- Real-time updates cho admin

### 4. **Quản Lý Kho Bãi**
- Lưu trữ vị trí GIS, người quản lý, contact
- Gợi ý route tự động
- Tính năng nearby warehouse search

### 5. **Quản Lý Phương Tiện & Tài Xế**
- Đăng ký xe với thông tin CCCD
- Liên kết tài xế và phương tiện
- Theo dõi status (Active/Inactive/On Delivery)
- Dashboard quản lý

### 6. **Hệ Thống Khuyến Mãi**
- Mã khuyến mãi với ngày hiệu lực
- Discount type: % hoặc VND cố định
- Min order amount checking
- Max usage tracking
- Auto-grant discount cho milestone

### 7. **Mô-đun Tin Tức & Tuyển Dụng**
- Publish tin tức với ảnh featured
- Tuyên dụng công khai với salary range
- Quản lý đơn ứng tuyển
- Email notifications

### 8. **API REST đầy đủ**
- 9 ViewSets (Orders, Vehicles, Warehouses, etc.)
- 20+ custom actions
- Pagination, filtering, searching
- Permission-based access

## 📋 Yêu Cầu & Chuẩn Bị

### Công Nghệ Stack
- **Backend:** Django 5.2.12 + Django REST Framework
- **Frontend:** Bootstrap 5 + Leaflet.js + Vanilla JS
- **Database:** SQLite (dev) / PostgreSQL (prod)
- **Maps:** Leaflet.js + OpenStreetMap
- **Email:** SMTP (Gmail/Mailtrap)

### Python Packages
```
Django==5.2.12
djangorestframework==3.14.0
django-crispy-forms==2.1
crispy-bootstrap5==0.7
django-filter==23.4
Pillow==10.0.0
geopy==2.3.0
python-decouple==3.8
```

## 🔧 Cài Đặt & Chạy

### 1. Clone Project
```bash
git clone <repository>
cd logistics_gis
```

### 2. Tạo Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

### 4. Chạy Migrations
```bash
python manage.py migrate
```

### 5. Khởi Tạo Dữ Liệu GIS
```bash
python manage.py init_gis_data
```

Lệnh này sẽ tạo:
- 4 Warehouses (Hà Nội x2, Hải Phòng, TP.HCM)
- 9 Price List entries
- 3 Promotion codes (SUMMER2026, WELCOME500K, NEWYEAR2026)

### 6. Tạo Admin User
```bash
python manage.py createsuperuser
```

### 7. Chạy Server
```bash
python manage.py runserver
```

Truy cập:
- 🏠 **Home:** http://localhost:8000/
- 🛠️ **Admin:** http://localhost:8000/admin/
- 📦 **Create Order:** http://localhost:8000/create-order/
- 📍 **Track Order:** http://localhost:8000/track-order/
- 📡 **API:** http://localhost:8000/api/

## 🗺️ GIS Map Integration

### Trang Tạo Đơn Hàng (`/create-order/`)

**Quy Trình:**
1. Bản đồ Leaflet được load tại Hà Nội (21.0285, 105.8542), zoom 13
2. User click lần 1: Chọn pickup point (marker xanh)
3. User click lần 2: Chọn delivery point (marker đỏ)
4. Tự động:
   - Vẽ polyline xanh nối 2 điểm
   - Tính khoảng cách Haversine
   - Call API `/api/orders/` để tính giá
   - Hiển thị breakdown giá (base + additional + discount)
   - Gợi ý số kho cần qua

**Code HTML:**
```html
<div id="map"></div>
<input type="hidden" id="pickup_lat" name="pickup_lat">
<input type="hidden" id="pickup_lng" name="pickup_lng">
<input type="hidden" id="delivery_lat" name="delivery_lat">
<input type="hidden" id="delivery_lng" name="delivery_lng">

<script src="{% static 'js/map_gis.js' %}"></script>
<script>
  GISMap.initialize('map');
</script>
```

**Functions:**
- `GISMap.initialize(elementId)` - Init map
- `GISMap.calculatePrice()` - Gọi API tính giá
- `GISMap.applyPromotion(code)` - Áp dụng mã khuyến mãi
- `GISMap.reset()` - Reset bản đồ

### Trang Theo Dõi (`/track-order/`)

**Quy Trình:**
1. User nhập mã đơn hàng
2. Hiển thị:
   - Thông tin khách hàng & người nhận
   - Bản đồ với route pickup → delivery
   - Timeline tracking các điểm kho
   - Real-time updates từ admin
3. Auto-refresh mỗi 30 giây

**Timeline Status:**
- 🟡 PENDING: Chờ check-in
- 🟢 CHECKED_IN: Đã điểm danh
- 🔵 IN_TRANSIT: Đang vận chuyển
- ✅ DELIVERED: Đã giao

## 📊 Database Schema

### Core Models

```
User (extends AbstractUser)
├── role: [USER, ADMIN, DRIVER]
├── phone_number
├── id_card_number
├── date_of_birth
├── email_verified: boolean
├── address (with ward, district, city)
└── @property age: calculated

Order
├── code: auto-generated (LOG-{year}-{4random})
├── customer_name, phone, address
├── delivery_point (address)
├── pickup_lat, pickup_lng, delivery_lat, delivery_lng
├── distance_km: calculated
├── base_price, additional_price, discount_amount, total_price
├── applied_promotion: FK Promotion (nullable)
├── status: [PENDING, PROCESSING, IN_TRANSIT, DELIVERED, CANCELLED]
├── payment_status: [PAID, UNPAID]
├── created_by: FK User
├── assigned_vehicle: FK Vehicle (nullable)
└── product_type, product_size, order_type

OrderTracking (✨ Key for multi-warehouse)
├── order: FK Order
├── warehouse: FK Warehouse
├── sequence: int (1, 2, 3...)
├── status: [PENDING, CHECKED_IN, IN_TRANSIT, DELIVERED]
├── checked_in_at: datetime
├── checked_in_by: FK User
├── notes: text
└── check_in(user, notes): method

OrderTrackingLog (📝 Audit trail)
├── order: FK Order
├── warehouse: FK Warehouse
├── action: [CHECK_IN, IN_TRANSIT, DELIVERED, CANCELLED]
├── user: FK User
├── notes: text
└── created_at: auto

Warehouse
├── name, address
├── manager_name, manager_phone
├── lat, lng (GIS coordinates)
└── timestamps

Vehicle
├── name, plate_number
├── driver_name, driver_birth_year
├── driver_id_card
├── vehicle_type
├── lat, lng
├── status: [ACTIVE, INACTIVE, ON_DELIVERY]
└── managed by: admin dashboard

PriceList
├── order_type: [STANDARD, EXPRESS, BULK]
├── distance_from, distance_to: Decimal (km)
├── base_price, per_km_price
└── Lookup table for pricing

Promotion
├── code: unique (e.g., SUMMER2026)
├── discount_type: [PERCENTAGE, FIXED]
├── discount_value: Decimal
├── min_order_amount
├── max_usage, usage_count
├── is_active, start_date, end_date
├── is_valid(): method
└── calculate_discount(amount): method

UserDiscount
├── user: FK User
├── promotion: FK Promotion
├── granted_at, is_used
└── used_in_order: FK Order

News
├── title, slug
├── content: RichTextField
├── featured_image: ImageField
├── author: FK User
├── is_published, published_at
└── timestamps

Recruitment
├── position, slug
├── description, requirements
├── salary_from, salary_to
├── is_active
└── timestamps

JobApplication
├── recruitment: FK Recruitment
├── applicant_name, email, phone
├── cv_file: FileField
├── cover_letter
├── status: [PENDING, REVIEWED, ACCEPTED, REJECTED]
├── reviewed_by: FK User
├── reviewed_at
└── notes
```

## 🔌 REST API Endpoints

### Base URL: `/api/`

#### Orders
```
GET    /orders/                          - List user's orders
POST   /orders/                          - Create new order
GET    /orders/{id}/                     - Order detail
POST   /orders/{id}/calculate-price/    - Recalculate pricing
GET    /orders/{id}/track/               - Get tracking history
POST   /orders/suggest-route/            - Get suggested warehouses
```

#### Vehicles
```
GET    /vehicles/                        - List all vehicles
GET    /vehicles/available/              - Get available (not on delivery)
```

#### Warehouses
```
GET    /warehouses/                      - List all warehouses
GET    /warehouses/nearby/               - Nearby search (?lat=&lng=&radius=)
```

#### Tracking
```
GET    /order-trackings/                 - Get trackings (?order_id=)
POST   /order-trackings/{id}/check-in/  - Check-in warehouse
```

#### Content
```
GET    /news/                            - Public news
GET    /recruitment/                     - Job listings
POST   /job-applications/               - Submit application
```

#### Pricing
```
GET    /price-lists/                     - Price table entries
POST   /promotions/validate/            - Validate promo code
```

**Example Request:**
```bash
# Calculate price
curl -X POST http://localhost:8000/api/orders/1/calculate-price/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: token" \
  -d '{"promotion_code": "SUMMER2026"}'

# Check-in warehouse
curl -X POST http://localhost:8000/api/order-trackings/5/check-in/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: token" \
  -d '{"notes": "Kiểm tra hàng hoàn tất"}'

# Validate promotion
curl -X POST http://localhost:8000/api/promotions/validate/ \
  -H "Content-Type: application/json" \
  -d '{"code": "SUMMER2026", "order_amount": 500000}'
```

## 📧 Email Configuration

### Mailtrap (Development)
```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'sandbox.smtp.mailtrap.io'
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_user@mailtrap.io'
EMAIL_HOST_PASSWORD = 'your_password'
```

### Gmail (Production)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'app_password_16_chars'
```

**Generate Gmail App Password:**
1. Google Account → Security
2. App passwords (requires 2FA)
3. Select "Mail" and "Windows"
4. Copy 16-char password

### Usage
```python
from core.services import EmailService

# Send confirmation
EmailService.send_order_confirmation(order)

# Send tracking update
EmailService.send_order_tracking_update(order, tracking)
```

## 📱 Mobile & Responsive

- ✅ Bootstrap 5 responsive grid
- ✅ Mobile-friendly forms
- ✅ Touch-friendly map
- ✅ Print-friendly tracking page
- ✅ Native sharing (mobile)

## 🔒 Security Features

- ✅ CSRF protection on forms
- ✅ Permission-based API access
- ✅ User-specific order visibility
- ✅ Admin-only management pages
- ✅ Secure password hashing
- ✅ Session timeout (30 days)

## 🧪 Testing

### Run Tests
```bash
python manage.py test core
```

### Manual Testing

**Test Order Creation:**
1. Register new user
2. Go to `/create-order/`
3. Click map twice (pickup & delivery)
4. Verify distance and price calculated
5. Apply SUMMER2026 code
6. Submit and verify in `/track-order/`

**Test API:**
```bash
# List orders
curl http://localhost:8000/api/orders/

# Create order (with CSRF)
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: your_token" \
  -d '{...order_data...}'
```

## 📚 Project Structure

```
logistics_gis/
├── core/
│   ├── models.py               # 12 models (Order, User, Warehouse, etc.)
│   ├── forms.py                # 10 forms (GIS-integrated)
│   ├── views.py                # Views + create_order, track_order
│   ├── api_views.py            # 9 REST ViewSets
│   ├── serializers.py          # 11 DRF serializers
│   ├── services.py             # Business logic (GIS, Pricing, etc.)
│   ├── admin.py                # Custom admin for all models
│   ├── urls.py                 # Web routes
│   ├── api_urls.py             # API routes
│   ├── management/
│   │   └── commands/
│   │       └── init_gis_data.py    # Init warehouses, pricing, promos
│   └── migrations/
├── logistics_gis/
│   ├── settings.py             # GIS, email, DRF config
│   ├── urls.py                 # Main URL router
│   └── wsgi.py
├── templates/core/
│   ├── base.html               # Bootstrap navbar + footer
│   ├── home.html               # Landing page
│   ├── create_order.html       # GIS map + form
│   └── track_order.html        # Timeline tracking
├── static/
│   ├── js/
│   │   ├── map_gis.js          # Leaflet integration (400+ lines)
│   │   └── main.js             # Utilities
│   └── css/
│       └── style.css           # Theme + responsive
└── requirements.txt            # 17 packages
```

## 🚢 Deployment (Production)

### Checklist
- [ ] Set `DEBUG = False` in settings
- [ ] Set `ALLOWED_HOSTS = ['yourdomain.com']`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure email (Gmail/Mailtrap)
- [ ] Set up static files collection: `python manage.py collectstatic`
- [ ] Use Gunicorn + Nginx
- [ ] Set up HTTPS/SSL
- [ ] Configure CORS if needed

### Quick Deploy (Heroku)
```bash
heroku login
heroku create your-app-name
heroku addons:create heroku-postgresql:hobby-dev
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

## 📖 API Documentation (Auto-generated)

Access via DRF Browsable API at `/api/` with nice HTML interface.

## 🐛 Troubleshooting

### Map not loading?
- Check browser console for errors
- Verify Leaflet CDN URLs are accessible
- Ensure lat/lng are decimals (-90 to 90, -180 to 180)

### Price not calculating?
- Check PriceList entries: `python manage.py shell`
  ```python
  from core.models import PriceList
  PriceList.objects.all().values()
  ```
- Verify distance calculation works
- Check promotion code validity

### Email not sending?
- Test settings: `python manage.py shell`
  ```python
  from django.core.mail import send_mail
  send_mail('Test', 'Body', 'from@example.com', ['to@example.com'])
  ```
- Check SMTP credentials
- Verify firewall/ISP blocking ports

## 📝 License

MIT License - Free to use and modify

## 👥 Contributors

- Development Team: Logistics GIS Team
- Contact: support@logisticsgis.com

## 🎯 Roadmap

- [ ] Payment gateway integration (Stripe, VNPay)
- [ ] SMS notifications
- [ ] Mobile app (React Native/Flutter)
- [ ] Real-time WebSocket updates
- [ ] Advanced route optimization
- [ ] Driver app with GPS tracking
- [ ] Customer notifications (SMS/Push)
- [ ] Analytics dashboard

---

**Made with ❤️ for Logistics Management**
