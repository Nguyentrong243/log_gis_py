# Hướng Dẫn Sử Dụng Bảng Điều Khiển Admin Logistics GIS

## 📊 Tổng Quan

Bảng điều khiển admin mới được thiết kế để quản lý toàn bộ hệ thống logistics trong một giao diện duy nhất. Hệ thống hỗ trợ:

- ✅ Quản lý phương tiện vận chuyển
- ✅ Quản lý kho bãi
- ✅ Quản lý tài xế
- ✅ Quản lý đơn hàng multi-warehouse
- ✅ Check-in và tracking lô hàng

## 🎯 Tính Năng Chính

### 1. Quản Lý Phương Tiện (Vehicles)

**Thông Tin Hiển Thị:**
- Tên phương tiện
- Biển số xe
- Loại xe
- **Tên Tài Xế** ⭐
- **Tuổi Tài Xế** (tính toán từ năm sinh) ⭐
- **CCCD Tài Xế** ⭐
- Trạng thái (Active, On Delivery, Inactive)

**Hành Động:**
- 🔍 Xem chi tiết
- ✏️ Sửa thông tin
- 🗑️ Xóa phương tiện
- 🆕 **Thêm phương tiện** (không giới hạn, có thể thêm vô hạn)

**Endpoint:**
```
GET  /vehicles/                      # Danh sách phương tiện
GET  /vehicles/<id>/                 # Chi tiết phương tiện
POST /vehicles/add/                  # Thêm phương tiện
POST /vehicles/<id>/edit/            # Sửa phương tiện
POST /vehicles/<id>/delete/          # Xóa phương tiện
```

### 2. Quản Lý Kho Bãi (Warehouses)

**Thông Tin Hiển Thị:**
- **Tên Kho** ⭐
- **Địa Chỉ** ⭐
- **Người Quản Lý Kho** ⭐
- **Số Điện Thoại Quản Lý** ⭐
- Tọa độ GIS (Lat, Lng)

**Hành Động:**
- 🔍 Xem chi tiết
- ✏️ Sửa thông tin
- 🗑️ Xóa kho
- 🆕 **Thêm kho** (không giới hạn)

**Endpoint:**
```
GET  /warehouses/                    # Danh sách kho
GET  /warehouses/<id>/               # Chi tiết kho
POST /warehouses/add/                # Thêm kho
POST /warehouses/<id>/edit/          # Sửa kho
POST /warehouses/<id>/delete/        # Xóa kho
```

### 3. Quản Lý Tài Xế (Drivers)

**Thông Tin Hiển Thị:**
- **Tên Tài Xế** ⭐
- **Ngày Sinh** ⭐
- **Tuổi** (tính toán tự động) ⭐
- **CCCD** ⭐
- **Số Điện Thoại** ⭐
- **Địa Chỉ** ⭐
- Trạng thái (Online, Offline, Busy)

**Hành Động:**
- 🔍 Xem thông tin cá nhân chi tiết
- ✏️ Sửa thông tin
- 🆕 **Thêm tài xế** (không giới hạn)

**Endpoint:**
```
GET  /drivers/                       # Danh sách tài xế (từ users có role=DRIVER)
GET  /drivers/<id>/                  # Chi tiết tài xế
POST /drivers/<id>/edit/             # Sửa thông tin tài xế
```

### 4. Quản Lý Đơn Hàng Multi-Warehouse ⭐ (Tính Năng Chính)

**Mô Hình Hoạt Động:**

Một đơn hàng từ TPHCM tới Nam Định sẽ đi qua nhiều kho:

```
Kho A (TPHCM)  →  Kho B (Hải Dương)  →  Kho C (Hà Nội)  →  Kho D (Nam Định)
```

Tại mỗi kho, admin cần **check-in** để xác nhận:
1. Lô hàng đã đến kho
2. Kiểm tra và xác nhận hàng hóa
3. Cho phép xe vận chuyển chuyển tiếp tới kho tiếp theo

**Thông Tin Hiển Thị:**
- Mã Đơn Hàng
- Tên Khách Hàng
- Điểm Nhận
- Điểm Giao
- Trạng Thái Đơn (Pending, Approved, In Progress, Delivered)
- **Kho Hiện Tại**

**Tabs:**
- 📋 Tất Cả Đơn
- ⏳ Chờ Xử Lý (PENDING)
- 🚚 Đang Vận Chuyển (IN_PROGRESS)
- ✅ Đã Giao (DELIVERED)

**Endpoint:**
```
GET  /orders/tracking/<order_id>/    # Xem lộ trình chi tiết
POST /orders/checkin/<tracking_id>/  # Check-in tại kho
```

### 5. Lộ Trình Giao Hàng (Order Tracking Detail) ⭐

**Chi Tiết Đơn Hàng:**
- Mã đơn, tên khách hàng, số điện thoại
- Điểm nhận, điểm giao
- Giá tiền, loại hàng, kích cỡ

**Timeline Vận Chuyển:**
- Hiển thị tất cả kho trong lộ trình
- Trạng thái mỗi kho (Pending, Checked-in, In Transit, Delivered)
- Thời gian check-in
- Ghi chú tại mỗi kho

**Lịch Sử Hoạt Động:**
- Tất cả hành động check-in, vận chuyển
- Người thực hiện
- Thời gian
- Ghi chú

**Endpoint:**
```
GET /orders/tracking/<order_id>/     # Xem lộ trình chi tiết
```

## 🔄 Quy Trình Hoạt Động Multi-Warehouse

### Bước 1: Tạo Đơn Hàng
```
Admin123 tạo đơn hàng với các kho trung chuyển
Mã Đơn: LOG-2026-0001
Lộ trình: Kho A → Kho B → Kho C
```

### Bước 2: Tạo Tracking cho Mỗi Kho
```
Sequence 1: Kho A - Status: PENDING
Sequence 2: Kho B - Status: PENDING
Sequence 3: Kho C - Status: PENDING
```

### Bước 3: Check-in Tại Kho
```
Khi xe đến Kho A:
- Admin Kho A check-in → Trạng thái → CHECKED_IN
- System tạo log: "LOG-2026-0001 đã đến Kho A vào 10:30"
- Cho phép xe chuyển sang Kho B

Khi xe đến Kho B:
- Admin Kho B check-in → Trạng thái → CHECKED_IN
- System tạo log: "LOG-2026-0001 đã đến Kho B vào 14:15"
- Cho phép xe chuyển sang Kho C

Khi xe đến Kho C:
- Admin Kho C check-in → Trạng thái → DELIVERED
- Đánh dấu đơn hàng là DELIVERED
- Hoàn tất lộ trình
```

### Bước 4: Theo Dõi Thực Thời
- Admin123 xem dashboard → Đơn hàng → Tracking
- Xem tất cả các bước đã thực hiện
- Xem lịch sử hoạt động chi tiết

## 📱 Hướng Dẫn Sử Dụng

### Truy Cập Dashboard
```
URL: http://yourdomain.com/admin-dashboard/
Yêu cầu: Admin role
```

### Tìm Kiếm
- **Tìm phương tiện**: Theo tên, biển số, tên tài xế
- **Tìm kho**: Theo tên kho, vị trí
- **Tìm tài xế**: Theo tên, số điện thoại, CCCD
- **Tìm đơn hàng**: Theo mã đơn, tên khách hàng

### Thêm Thông Tin Mới
Để thêm phương tiện, kho, hoặc tài xế mới (không giới hạn):
1. Click nút **Thêm [Tên]** ở mỗi section
2. Điền đầy đủ thông tin
3. Click **Lưu**
4. Thông tin sẽ được hiển thị trong danh sách

### Check-in Lô Hàng
1. Vào tab **Check-in Kho Bãi**
2. Xem danh sách đơn hàng chờ check-in
3. Click **Check-in**
4. Nhập ghi chú (nếu cần)
5. Xác nhận
6. Lô hàng được chuyển sang kho tiếp theo

## 📊 Thống Kê

Dashboard hiển thị 4 chỉ số chính:
- 🚗 **Tổng Phương Tiện**: Tất cả xe trong hệ thống
- 🏢 **Tổng Kho**: Tất cả kho bãi liên kết
- 👨 **Tổng Tài Xế**: Tất cả tài xế
- 📦 **Tổng Đơn Hàng**: Tất cả đơn hàng

## 🗄️ Cơ Sở Dữ Liệu

### Các Bảng Chính:

**Vehicle**
```
- id, name, driver_name, driver_birth_year, plate_number
- vehicle_type, lat, lng, status
```

**Warehouse**
```
- id, name, address, manager_name, manager_phone
- lat, lng, created_at, updated_at
```

**User (Driver)**
```
- id, username, first_name, last_name, email
- phone_number, id_card_number, date_of_birth
- address, role='DRIVER'
```

**Order**
```
- id, code, customer_name, customer_phone
- pickup_point, delivery_point, status
- total_price, created_at, updated_at
```

**OrderTracking**
```
- id, order_id, warehouse_id, sequence, status
- checked_in_at, checked_in_by_id, notes
```

**OrderTrackingLog**
```
- id, order_id, warehouse_id, action, user_id
- notes, created_at
```

## 🔗 URLs Mapping

```
/admin-dashboard/                           # Bảng điều khiển chính
/vehicles/                                  # Danh sách phương tiện
/vehicles/<id>/                             # Chi tiết phương tiện
/vehicles/add/                              # Thêm phương tiện
/vehicles/<id>/edit/                        # Sửa phương tiện
/warehouses/                                # Danh sách kho
/warehouses/<id>/                           # Chi tiết kho
/warehouses/add/                            # Thêm kho
/warehouses/<id>/edit/                      # Sửa kho
/orders/tracking/<order_id>/                # Xem lộ trình
/orders/checkin/<tracking_id>/              # Check-in lô hàng
```

## ⚙️ Cấu Hình

Không cần cấu hình thêm. Hệ thống sử dụng:
- Django ORM
- Bootstrap 5 (CSS)
- Font Awesome (Icons)
- JavaScript vanilla

## 🐛 Troubleshooting

### Không thấy dashboard
- Kiểm tra role user = 'ADMIN'
- URL đúng: `/admin-dashboard/`

### Check-in không hoạt động
- Kiểm tra user có role admin kho
- Kiểm tra order có tracking
- Xem console Django cho lỗi

### Dữ liệu không hiển thị
- Clear cache browser: Ctrl+Shift+Delete
- Reload trang
- Kiểm tra database connection

## 📝 Ghi Chú

- Tất cả thời gian lưu theo UTC+7
- Check-in không thể hoàn tác, chỉ có thể xem lại trong lịch sử
- Xóa kho/xe/tài xế sẽ ảnh hưởng đến order nếu đã tham chiếu

## 🚀 Cập Nhật Tương Lai

Các tính năng sẽ được thêm:
- 📊 Báo cáo thống kê chi tiết
- 📧 Thông báo email khi check-in
- 🗺️ Bản đồ GIS thực thời
- 🔔 Cảnh báo khi quá hạn
- 📱 Mobile app

---

**Phiên bản:** 1.0  
**Ngày cập nhật:** 20/04/2026  
**Tác giả:** Logistics GIS Team
