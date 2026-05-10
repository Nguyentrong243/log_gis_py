# Testing Guide - Logistics GIS

Hướng dẫn chi tiết để test toàn bộ tính năng của hệ thống.

## 🚀 Quick Start Test

### 1. Chuẩn Bị
```bash
# Activate venv
venv\Scripts\activate

# Run migrations
python manage.py migrate

# Init GIS data (warehouses, pricing, promos)
python manage.py init_gis_data

# Create superuser
python manage.py createsuperuser
# Username: admin, Email: admin@local.com, Password: admin123

# Run server
python manage.py runserver
```

Server chạy tại: http://localhost:8000

### 2. Test Accounts

```
Admin Account:
- Username: admin
- Password: admin123
- Role: ADMIN

Test User:
- Username: testuser
- Email: test@example.com
- Password: testpass123
```

## 🧪 Feature Testing

### 1️⃣ User Registration & Authentication

**Test Case 1.1: Registration with validation**
```
URL: http://localhost:8000/register/
Steps:
1. Click "Đăng Ký" button
2. Fill form:
   - Username: newuser123
   - Email: new@example.com
   - Phone: 0912345678
   - Password: Secure123!
   - Confirm: Secure123!
3. Submit form
4. Verify redirect to login page with success message
5. Login with new credentials

Expected: ✓ Account created, can login
```

**Test Case 1.2: Phone validation**
```
Fill Phone: "123" (invalid)
Submit → Should show error: "Số điện thoại phải có 10 chữ số"

Fill Phone: "0912345678" (valid)
Submit → Should pass validation
```

**Test Case 1.3: Email verification (optional)**
```
After registration:
- Check Django admin for email_verified status
- Should be False initially
- Email verification link sent (in Mailtrap sandbox)
```

### 2️⃣ GIS Map & Order Creation

**Test Case 2.1: Create order with map**
```
URL: http://localhost:8000/create-order/
Prerequisites: Login as testuser

Steps:
1. Page loads with Leaflet map centered on Hà Nội
2. Fill customer info:
   - Name: Nguyễn Văn A
   - Phone: 0987654321
3. Click map at one point (e.g., Ben Thanh Market)
   → Green marker appears, coordinates filled
4. Click another point (e.g., 5km away)
   → Red marker appears
   → Blue polyline drawn between points
   → Distance shows: ~5.2 km
   → Price calculated: Base + Additional
5. Fill recipient info:
   - Name: Tran Thi B
   - Phone: 0123456789
6. Select product type: "Hàng gửi"
7. Select service type: "Standard"
8. Optional: Apply promo code "SUMMER2026"
9. Click "Tạo Đơn Hàng"

Expected Results:
✓ Map loads with OSM tiles
✓ Markers placed correctly
✓ Distance calculated (Haversine formula)
✓ Price breakdown shown:
  - Giá cơ sở: 30,000 VND
  - Phí thêm: ~25,000 VND
  - Giảm giá: (if promo applied)
  - TỔNG: ~55,000 VND
✓ Order created with auto-generated code
✓ Order tracking route created (1-3 warehouses)
✓ Redirect to tracking page
```

**Test Case 2.2: Reset map**
```
1. After placing both markers, click "Reset Bản Đồ" button
2. Both markers removed
3. Price display reset to 0
4. Form fields cleared
5. Ready for new selection
```

**Test Case 2.3: Distance calculation accuracy**
```
Test coordinates:
- Hanoi City Center (21.0285, 105.8542)
- Hanoi Phong Chay (21.0410, 105.7893)
- Expected distance: ~8-9 km

Verify:
1. Enter coordinates manually or click map
2. Distance displayed: 8.X km
3. Price calculated based on tier:
   - 0-10km Standard: 30,000 base + (8 * 5,000) = 70,000 VND
```

### 3️⃣ Pricing Engine

**Test Case 3.1: Tiered pricing**
```
Create 3 orders with different distances:

Order 1: 5km (0-10km tier)
- Base: 30,000 → Total: ~55,000 VND

Order 2: 25km (10-30km tier)
- Base: 50,000 → Total: ~110,000 VND

Order 3: 80km (30-100km tier)
- Base: 80,000 → Total: ~230,000 VND

Verify: Each order uses correct pricing tier
```

**Test Case 3.2: Promotion codes**
```
Code 1: SUMMER2026 (20% discount)
- Order amount: 50,000 VND
- Discount: 10,000 VND (20%)
- Final: 40,000 VND

Code 2: WELCOME500K (fixed 50,000)
- Min order: 500,000 VND
- Apply to 55,000 order → Should fail
- Apply to 600,000 order → OK, Final: 550,000

Code 3: Expired code → Should show "không hợp lệ"
```

**Test Case 3.3: Max usage tracking**
```
1. Check promotion: SUMMER2026 has max_usage=100
2. Create 5 orders with same promo
3. Usage count increases: 1, 2, 3, 4, 5
4. After max_usage reached → Cannot apply
```

### 4️⃣ Order Tracking & Timeline

**Test Case 4.1: Track existing order**
```
URL: http://localhost:8000/track-order/

Steps:
1. Enter order code from previous test (e.g., LOG-2026-1234)
2. Click "Tìm Kiếm"

Expected Display:
✓ Order code: LOG-2026-1234
✓ Status badge: PENDING / PROCESSING / IN_TRANSIT / DELIVERED
✓ Customer info: Name, phone, addresses
✓ Recipient info: Name, phone
✓ Product info: Type, size, service type
✓ Pricing: Distance, base price, total
✓ Map with route from pickup to delivery
✓ Timeline with warehouses:
  - Warehouse 1: Status icon, timestamp
  - Warehouse 2: Status icon, timestamp
  - Warehouse 3: Status icon, timestamp
```

**Test Case 4.2: Multi-warehouse routing**
```
Test different distances:

Order A: 5km (0-20km range)
→ Direct delivery (0 warehouses between)
→ Timeline shows: Pickup → Delivery

Order B: 60km (20-100km range)
→ Via 1 hub warehouse
→ Timeline shows: Pickup → Hub → Delivery

Order C: 250km (>100km)
→ Via 2 hub warehouses
→ Timeline shows: Pickup → Hub1 → Hub2 → Delivery

Verify: Correct warehouse routing based on distance
```

**Test Case 4.3: Real-time updates (Admin)**
```
As Admin (http://localhost:8000/admin/):
1. Navigate to Order Tracking
2. Click "Check In" for warehouse 1
3. Set status: CHECKED_IN
4. Add notes: "Kiểm tra hàng"
5. Save

Back on tracking page (http://localhost:8000/track-order/):
6. Timeline updates (may need refresh or auto-update in 30s)
7. Warehouse 1 shows: ✅ CHECKED_IN, timestamp, notes
8. Next warehouse auto-marked: PENDING
```

### 5️⃣ Admin Dashboard

**Test Case 5.1: Login to admin**
```
URL: http://localhost:8000/admin/
Credentials: admin / admin123

Expected:
✓ Django admin interface loads
✓ Custom admin classes for 14 models visible:
  - Users (with role display)
  - Orders (with status colors)
  - Vehicles (with driver info)
  - Warehouses
  - Order Tracking (with status timeline)
  - Order Tracking Logs (audit trail)
  - Price Lists
  - Promotions (usage tracking)
  - News
  - Recruitment
  - Job Applications
```

**Test Case 5.2: Order management**
```
1. Click "Orders" in admin
2. List view shows: Code, Customer, Status (colored), Distance, Price, Payment Status (colored)
3. Click order to edit:
   - View all fields including GIS coords
   - Change status
   - Assign vehicle
   - Apply discount
   - Save
4. Verify changes reflected in tracking page
```

**Test Case 5.3: Warehouse management**
```
1. Click "Warehouses" in admin
2. List view shows: Name, Address, Manager, Manager Phone
3. Add new warehouse:
   - Name: "Kho Đà Nẵng"
   - Address: "Đà Nẵng"
   - Manager: "Tran Van X"
   - Phone: "0987654321"
   - Lat: 16.0544, Lng: 108.2022
4. Save
5. New warehouse appears in suggestions for future orders
```

**Test Case 5.4: Price list management**
```
1. Click "Price Lists" in admin
2. View all tiers (Standard/Express/Bulk)
3. Edit STANDARD 10-30km tier:
   - Base price: 50,000 → 55,000
   - Per km: 4,000 → 3,500
4. Save
5. Create new order with 25km → New pricing applies
```

### 6️⃣ REST API

**Test Case 6.1: API authentication**
```
# List orders (requires login)
curl -b cookies.txt \
  http://localhost:8000/api/orders/

# Response should show JSON list of user's orders
```

**Test Case 6.2: Create order via API**
```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Content-Type: application/json" \
  -H "X-CSRFToken: $(get_csrf_token)" \
  -d '{
    "customer_name": "Nguyen Van A",
    "customer_phone": "0912345678",
    "pickup_lat": "21.0285",
    "pickup_lng": "105.8542",
    "delivery_lat": "21.0410",
    "delivery_lng": "105.7893",
    "delivery_point": "Pham Ngu Lao, HCMC",
    "order_type": "STANDARD",
    "product_type": "DOCUMENT",
    "product_size": "SMALL",
    "recipient_name": "Tran Thi B",
    "recipient_phone": "0123456789"
  }'

Expected: 201 Created with:
- Order code auto-generated
- Distance calculated
- Price breakdown included
```

**Test Case 6.3: Calculate price endpoint**
```bash
curl -X POST http://localhost:8000/api/orders/1/calculate-price/ \
  -H "Content-Type: application/json" \
  -d '{"promotion_code": "SUMMER2026"}'

Expected: {
  "distance_km": 8.5,
  "base_price": 30000,
  "additional_price": 42500,
  "discount_amount": 14550,
  "total_price": 57950
}
```

**Test Case 6.4: Suggest route endpoint**
```bash
curl -X POST http://localhost:8000/api/orders/suggest-route/ \
  -H "Content-Type: application/json" \
  -d '{
    "pickup_lat": "21.0285",
    "pickup_lng": "105.8542",
    "delivery_lat": "10.8231",
    "delivery_lng": "106.6843"
  }'

Expected: {
  "suggested_route": [
    {"id": 1, "name": "Kho Hà Nội 1", ...},
    {"id": 2, "name": "Kho TP.HCM", ...}
  ]
}
```

**Test Case 6.5: Tracking endpoint**
```bash
curl http://localhost:8000/api/orders/1/track/ \
  -H "Authorization: Bearer token"

Expected: {
  "order_code": "LOG-2026-1234",
  "current_status": "IN_TRANSIT",
  "trackings": [...],
  "logs": [...]
}
```

### 7️⃣ Warehouses & Vehicles

**Test Case 7.1: Nearby warehouse search**
```bash
curl "http://localhost:8000/api/warehouses/nearby/?lat=21.0285&lng=105.8542&radius=50"

Expected: [{
  "id": 1,
  "name": "Kho Hà Nội 1",
  "distance": 0.5,
  "address": "..."
}]

Result: Sorted by distance ascending, within 50km
```

**Test Case 7.2: Vehicle management**
```
Admin → Vehicles:
1. List all vehicles
2. View status: ACTIVE (green), INACTIVE (gray), ON_DELIVERY (blue)
3. Edit vehicle:
   - Assign to order
   - Change status
4. View driver info: Name, birth year, ID card, phone

Verify: Display normalization (Vehicle display_name is clean)
```

### 8️⃣ Content Management

**Test Case 8.1: News publishing**
```
Admin → News:
1. Click "Add News"
2. Fill:
   - Title: "Khuyến mãi mùa hè 2026"
   - Slug: auto-generated
   - Content: "Nội dung tin tức"
   - Featured Image: Upload
   - Author: auto-filled
   - is_published: ✓
3. Save
4. Verify on homepage: Latest news displayed
```

**Test Case 8.2: Job posting**
```
Admin → Recruitment:
1. Click "Add Recruitment"
2. Fill:
   - Position: "Tài xế giao hàng"
   - Description: "Yêu cầu..."
   - Salary: 5,000,000 - 8,000,000
   - is_active: ✓
3. Save
4. Access /recruitment/ page → Listing shows all active jobs
```

**Test Case 8.3: Job application**
```
Public:
1. Go to /recruitment/ page
2. Click "Ứng Tuyển" on position
3. Fill form:
   - Name: "Tran Van X"
   - Email: "x@example.com"
   - Phone: "0987654321"
   - CV: Upload PDF/DOC
   - Cover letter: Optional
4. Submit

Admin:
1. Check Order Management → Job Applications
2. View applicant details
3. Update status: PENDING → REVIEWED → ACCEPTED/REJECTED
4. Add review notes
5. System sends email confirmation
```

## 📊 Load Testing

### Database Checks
```python
# Check data consistency
python manage.py shell

from core.models import *
# Count records
Order.objects.count()
OrderTracking.objects.count()
User.objects.count()

# Test service functions
from core.services import GISDistanceService, PricingService
distance = GISDistanceService.haversine_distance(21.0285, 105.8542, 10.8231, 106.6843)
print(f"Distance: {distance} km")  # Should be ~1000km

price = PricingService.calculate_price(distance, "STANDARD")
print(f"Price: {price}")
```

### Performance Testing
```bash
# Test with Apache Bench
ab -n 100 -c 10 http://localhost:8000/

# Test API with load
ab -n 1000 -c 50 http://localhost:8000/api/orders/
```

## 🔍 Bug Hunting Checklist

- [ ] Map loads on all browsers (Chrome, Firefox, Safari, Edge)
- [ ] Mobile responsive (iPad, iPhone, Android)
- [ ] Distance calculation accurate for all distances (5km, 50km, 1000km)
- [ ] Price calculation matches tier expectations
- [ ] Promotion codes apply correctly
- [ ] Order codes are unique
- [ ] Warehouse routing correct for <20km, 20-100km, >100km
- [ ] Timeline displays all warehouses in correct order
- [ ] Check-in updates status instantly
- [ ] Email sending works (check Mailtrap)
- [ ] Admin can edit all fields
- [ ] User can only see own orders
- [ ] API pagination works (20 per page)
- [ ] Filtering works on admin lists
- [ ] Sorting works on admin lists
- [ ] Search works for order codes and customer names

## 📝 Test Results Template

```
Test Date: ___________
Tester: ___________
Django Version: 5.2.12
Database: SQLite

Feature: ___________
Status: ✅ PASS / ❌ FAIL
Duration: ___ seconds
Notes:
_______________________________
_______________________________

Issues Found:
1. ___________
2. ___________
```

## 🎯 Coverage Goals

- [ ] 80%+ model tests
- [ ] 80%+ service tests
- [ ] 60%+ view tests
- [ ] All critical API endpoints
- [ ] UI functionality (manual)

---

**Happy Testing! 🚀**
