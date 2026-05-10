# 🚀 Quick Start - Logistics GIS

Hướng dẫn chạy hệ thống trong 5 phút.

## Yêu Cầu
- Python 3.9+
- pip / conda
- Git (optional)

## Cài Đặt (Windows)

### 1️⃣ Tạo Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 2️⃣ Cài Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Khởi Tạo Database
```bash
python manage.py migrate
```

### 4️⃣ Tạo Dữ Liệu GIS (Warehouses, Pricing, Promos)
```bash
python manage.py init_gis_data
```

Output:
```
✓ Tạo: Kho Hà Nội 1
✓ Tạo: Kho Hà Nội 2
✓ Tạo: Kho Hải Phòng
✓ Tạo: Kho TP. Hồ Chí Minh
✓ Tạo 9 bảng giá
✓ Tạo 3 mã khuyến mãi
✓ Khởi tạo dữ liệu thành công!
```

### 5️⃣ Tạo Admin User
```bash
python manage.py createsuperuser
```

Nhập:
- Username: `admin`
- Email: `admin@localhost.com`
- Password: `admin123` (or your choice)

### 6️⃣ Chạy Server
```bash
python manage.py runserver
```

Server chạy tại: **http://localhost:8000/**

## 🎯 Điểm Truy Cập Chính

| URL | Chức Năng |
|-----|----------|
| http://localhost:8000/ | Trang chủ |
| http://localhost:8000/create-order/ | Tạo đơn (GIS Map) |
| http://localhost:8000/track-order/ | Theo dõi đơn |
| http://localhost:8000/admin/ | Quản lý admin |
| http://localhost:8000/api/ | REST API (DRF) |

## 👤 Test Accounts

### Admin
```
Username: admin
Password: admin123
```

### Regular User (tự đăng ký)
```
Register: http://localhost:8000/register/
- Username: testuser
- Email: test@example.com
- Password: Secure123!
```

## 📱 Test Tính Năng

### 1️⃣ Tạo Đơn với GIS Map
```
1. Đăng nhập: http://localhost:8000/login/
2. Vào: http://localhost:8000/create-order/
3. Click bản đồ 2 lần (pickup + delivery)
4. Giá tự động tính
5. Submit
```

### 2️⃣ Theo Dõi Đơn
```
1. Vào: http://localhost:8000/track-order/
2. Nhập mã đơn (ví dụ: LOG-2026-1234)
3. Xem timeline tracking
```

### 3️⃣ Quản Lý Admin
```
1. Vào: http://localhost:8000/admin/
2. Login: admin / admin123
3. Thay đổi status đơn, kho, xe...
```

### 4️⃣ Dùng API
```bash
# List orders
curl http://localhost:8000/api/orders/

# Calculate price
curl -X POST http://localhost:8000/api/orders/1/calculate-price/ \
  -H "Content-Type: application/json" \
  -d '{"promotion_code": "SUMMER2026"}'

# Suggest route
curl -X POST http://localhost:8000/api/orders/suggest-route/ \
  -H "Content-Type: application/json" \
  -d '{
    "pickup_lat": "21.0285",
    "pickup_lng": "105.8542",
    "delivery_lat": "10.8231",
    "delivery_lng": "106.6843"
  }'
```

## 🎁 Mã Khuyến Mãi Có Sẵn

| Mã | Kiểu | Giá Trị | Min Order | Max Uses |
|----|------|--------|-----------|----------|
| SUMMER2026 | 20% | 20% | 100K | 100 |
| WELCOME500K | Fixed | 50K | 500K | 50 |
| NEWYEAR2026 | 15% | 15% | 200K | 200 |

Ví dụ: Tạo đơn 600K, apply SUMMER2026 → Thanh toán 480K

## 🗺️ GIS Map Features

- **Leaflet.js** + OpenStreetMap
- Click to select pickup point (xanh)
- Click to select delivery point (đỏ)
- Auto distance calculation (Haversine)
- Auto price calculation
- Polyline showing route
- Reset button

## 📊 Bảng Giá (Price List)

**STANDARD (tiêu chuẩn):**
- 0-10km: 30K base + 5K/km
- 10-30km: 50K base + 4K/km
- 30-100km: 80K base + 3K/km
- 100km+: 150K base + 2K/km

**EXPRESS (nhanh):**
- 0-10km: 50K base + 7K/km
- 10-30km: 80K base + 6K/km
- 30km+: 120K base + 4K/km

**BULK (dơi):**
- 0-50km: 100K base + 3K/km
- 50km+: 200K base + 1.5K/km

## 🏭 Kho Bãi (Warehouses)

4 kho đã được khởi tạo:

1. **Kho Hà Nội 1**
   - Địa chỉ: Thăng Long, Hoài Đức
   - Quản lý: Nguyễn Văn A

2. **Kho Hà Nội 2**
   - Địa chỉ: Trần Quốc Hoàn, Cầu Giấy
   - Quản lý: Trần Thị B

3. **Kho Hải Phòng**
   - Địa chỉ: Tiên Sơn, Tiên Lãng
   - Quản lý: Lê Văn C

4. **Kho TP. HCM**
   - Địa chỉ: Nguyễn Hữu Cảnh, Bình Thạnh
   - Quản lý: Phạm Việt D

## 🧪 Troubleshooting

### Map không load
```
✓ Kiểm tra browser console (F12)
✓ Đảm bảo internet connect
✓ Refresh page
✓ Thử browser khác
```

### Giá không tính
```
✓ Kiểm tra PriceList entries
  python manage.py shell
  from core.models import PriceList
  PriceList.objects.all().values()
  
✓ Đảm bảo chọn 2 điểm trên map
✓ Kiểm tra console cho lỗi API
```

### Không thể đăng nhập
```
✓ Kiểm tra username/password
✓ Đảm bảo user tồn tại
  python manage.py shell
  from core.models import User
  User.objects.all().values('username', 'email')
  
✓ Reset password nếu cần
```

### Database lỗi
```
✓ Reset migrations
  python manage.py migrate zero
  python manage.py migrate
  python manage.py init_gis_data
```

## 📚 Tài Liệu Chi Tiết

- **README_COMPLETE.md** - Tài liệu toàn diện
- **TESTING.md** - Hướng dẫn test
- **CHANGELOG.md** - Lịch sử phát triển

## 🎓 Hiểu Cơ Chế

### Order Creation Flow
```
User fills form + clicks map
    ↓
Frontend: Distance calculated (Haversine JS)
    ↓
POST /api/orders/
    ↓
Backend: Order.save() → auto code + GIS distance
    ↓
PricingService: Calculate tiered price
    ↓
WarehouseService: Suggest route (1-3 warehouses)
    ↓
OrderTrackingService: Create tracking for each warehouse
    ↓
EmailService: Send confirmation
    ↓
Redirect to tracking page
```

### Tracking Flow
```
Admin checks in warehouse → POST /api/order-trackings/{id}/check-in/
    ↓
OrderTracking.check_in() called
    ↓
Status: CHECKED_IN + timestamp
    ↓
OrderTrackingLog: Audit entry created
    ↓
Next warehouse auto-marked: PENDING
    ↓
If final warehouse → Order.status: DELIVERED
    ↓
Email notification sent
    ↓
Frontend: Timeline auto-updates
```

## 💡 Tips

1. **Dùng promo code trong tạo đơn**
   - Apply SUMMER2026 để giảm 20%
   - Min order 100K

2. **Kiểm tra tracking real-time**
   - Admin update status
   - Tracking page auto-refresh mỗi 30s

3. **Test API dễ dàng**
   - Truy cập /api/ để xem DRF interface
   - Click vào endpoints để test

4. **Admin là siêu user**
   - Có thể edit tất cả models
   - Có thể xem tất cả orders
   - Regular user chỉ thấy own orders

## 🚢 Deploy to Production

Sau khi test OK:

```bash
# Collect static files
python manage.py collectstatic

# Set DEBUG = False in settings.py
# Configure ALLOWED_HOSTS
# Use PostgreSQL instead of SQLite
# Use Gunicorn + Nginx
# Setup HTTPS/SSL
# Deploy to server (Heroku, AWS, etc.)
```

## ❓ Support

- Kiểm tra TESTING.md cho test cases chi tiết
- Kiểm tra README_COMPLETE.md cho API docs
- Xem admin interface tại /admin/
- Xem DRF browsable API tại /api/

---

**Ready to go! 🎉**

Enjoy using Logistics GIS!
