# Logistics GIS - Hướng Dẫn Các Tính Năng Quản Lý Mới

## 📋 Mục Lục
1. [Quản lý Phương tiện](#quản-lý-phương-tiện)
2. [Quản lý Kho bãi](#quản-lý-kho-bãi)
3. [Quản lý Tài xế](#quản-lý-tài-xế)
4. [Tracking Đơn hàng Multi-Warehouse](#tracking-đơn-hàng-multi-warehouse)

---

## 🚗 Quản Lý Phương Tiện

### Vị Trí: Menu Quản lý → Quản lý Phương tiện

### Chức Năng:
- **Xem danh sách phương tiện**: Hiển thị tất cả xe với thông tin tài xế, biển số, trạng thái
- **Chi tiết phương tiện**: Xem chi tiết tài xế (tên, tuổi, CCCD, năm sinh)
- **Xem đơn hàng**: Xem các đơn hàng hiện tại và lịch sử giao hàng của phương tiện
- **Thêm phương tiện mới**: Nút "+ Thêm phương tiện"
- **Sửa thông tin**: Chỉnh sửa tên xe, tài xế, biển số, loại xe
- **Xóa phương tiện**: Xóa phương tiện (kèm xác nhận)

### Thông Tin Hiển Thị:
```
Tên xe          | Tài xế      | Biển số  | Loại xe | Năm sinh | Trạng thái
Xe Máy A        | Nguyễn Văn A| 29X1234  | Xe máy  | 1990     | Hoạt động
```

### Trạng Thái Phương Tiện:
- ✅ **ACTIVE** - Hoạt động (sẵn sàng nhận đơn)
- 🔄 **ON_DELIVERY** - Đang giao hàng
- ❌ **INACTIVE** - Bất hoạt (không hoạt động)

---

## 🏭 Quản Lý Kho Bãi

### Vị Trí: Menu Quản lý → Quản lý Kho bãi

### Chức Năng:
- **Xem danh sách kho**: Hiển thị tất cả kho bãi liên kết
- **Chi tiết kho**: Xem thông tin kho + đơn hàng đang lưu tại kho
- **Thông tin kho**: Tên, địa chỉ, người quản lý, SĐT quản lý, tọa độ GIS
- **Thêm kho mới**: Nút "+ Thêm kho bãi" (để hợp tác với kho khác)
- **Sửa thông tin kho**: Cập nhật địa chỉ, quản lý, SĐT
- **Xóa kho**: Xóa kho khỏi hệ thống

### Thông Tin Kho Bãi:
```json
{
  "name": "Kho TPHCM",
  "address": "123 Đường ABC, Q1, TPHCM",
  "manager_name": "Trần Văn B",
  "manager_phone": "0901234567",
  "lat": 10.7769,
  "lng": 106.6966
}
```

### Trạng Thái Đơn Hàng Tại Kho:
- ⏳ **PENDING** - Chờ đến kho
- ✅ **CHECKED_IN** - Đã check-in
- 🚚 **IN_TRANSIT** - Đang vận chuyển
- 📦 **DELIVERED** - Đã giao

---

## 👨‍💼 Quản Lý Tài Xế

### Vị Trí: Menu Quản lý → Quản lý Tài xế

### Chức Năng:
- **Xem danh sách tài xế**: Liệt kê tất cả tài xế trong hệ thống
- **Chi tiết tài xế**: Xem thông tin cá nhân + phương tiện + đơn hàng
- **Thông tin cá nhân**:
  - Tên, Username
  - Tuổi (tính từ ngày sinh)
  - CCCD/CMT
  - Email, số điện thoại
  - Địa chỉ (Phường, Quận, Thành phố)

### Trạng Thái Tài Xế:
- 🟢 **ONLINE** - Sẵn sàng nhận đơn
- 🟡 **BUSY** - Đang bận (đang giao hàng)
- 🔴 **OFFLINE** - Ngoại tuyến

### Thống Kê:
- Số đơn đã giao (DELIVERED)
- Số đơn đang giao (APPROVED + IN_PROGRESS)
- Phương tiện được sử dụng
- Trạng thái hồ sơ (Đã hoàn thành / Chưa)

---

## 📍 Tracking Đơn Hàng Multi-Warehouse

### Vị Trí: Menu Quản lý → Tracking đơn hàng

### 🎯 Mục Đích:
Theo dõi lộ trình giao hàng khi đơn phải đi qua nhiều kho trung chuyển.

### Quy Trình Vận Chuyển Đa Kho:

```
Ví dụ: Giao từ TPHCM đến Nam Định

1. Kho A (TPHCM)
   ↓ [Check-in]
2. Kho B (Hà Nội) 
   ↓ [Check-in]
3. Kho C (Nam Định)
   ↓ [Check-in]
4. Tài xế giao cuối
   ↓ [Giao]
5. Khách hàng
```

### Các Trang Chính:

#### 1️⃣ Danh Sách Tracking Đơn Hàng
**URL**: `/order-tracking/`
- Xem tất cả đơn hàng đang tracking
- Filter theo trạng thái (Chờ, Check-in, Vận chuyển, Giao)
- Search theo mã đơn hoặc kho bãi
- Nút "Chi tiết" → xem lộ trình chi tiết
- Nút "Check-in" (nếu đơn chờ đến kho)

#### 2️⃣ Chi Tiết Lộ Trình Đơn Hàng
**URL**: `/order/<order_id>/tracking/`

**Hiển thị:**
- Thông tin đơn hàng (mã, khách, người nhận, giá)
- **Timeline lộ trình kho**: Hiển thị thứ tự các kho
  ```
  Kho 1: Kho A (TPHCM)
    Status: ✅ Đã check-in
    Check-in lúc: 20/04/2026 10:30
    Check-in bởi: Admin User
    
  Kho 2: Kho B (Hà Nội)
    Status: ⏳ Chờ đến kho
    
  Kho 3: Kho C (Nam Định)
    Status: ⏳ Chờ đến kho
  ```
- **Lịch sử tracking**: Bảng logs chi tiết tất cả hành động

#### 3️⃣ Check-in Lô Hàng Tại Kho
**URL**: `/order-tracking/<tracking_id>/checkin/`

**Quy Trình:**
1. Kho bãi nhận lô hàng
2. Kiểm tra tình trạng hàng hóa
3. Điền form check-in:
   - Chọn đơn hàng
   - Ghi chú tình trạng (vd: "Hàng nguyên vẹn, đầy đủ")
4. Nhấn **"Xác nhận check-in"**
5. Hệ thống tự động:
   - Cập nhật status thành CHECKED_IN
   - Ghi lại thời gian check-in
   - Chuyển đơn sang kho tiếp theo
   - Gửi log về admin tổng

#### 4️⃣ Tiếp Nhận Lô Hàng Tại Kho
**URL**: `/warehouse/<warehouse_id>/receive/`

**Chức Năng:**
- Xem tất cả lô hàng chờ tiếp nhận tại kho này
- Danh sách hiển thị: Mã đơn, khách hàng, loại hàng, người nhận
- Nút "Tiếp nhận" → vào form check-in
- Nút "Chi tiết" → xem lộ trình toàn bộ đơn

---

## 📊 Sơ Đồ Quy Trình Đơn Hàng Multi-Warehouse

```mermaid
┌─────────────────────────────────────────────────────────────┐
│                    ADMIN TẠO ĐƠN HÀNG                       │
│                   (Từ TPHCM → Nam Định)                     │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  HỆ THỐNG TỰ ĐỘNG TẠO LỘ TRÌNH QUA CÁC KHO                │
│  Route: Kho A (TPHCM) → Kho B (Hà Nội) → Kho C (Nam Định) │
└────────────────────┬────────────────────────────────────────┘
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
    ┌─────────┐ ┌─────────┐ ┌─────────┐
    │ Kho A   │ │ Kho B   │ │ Kho C   │
    │ TPHCM   │ │ Hà Nội  │ │ Nam Định│
    └────┬────┘ └────┬────┘ └────┬────┘
         │           │           │
         │ [Check-in]│           │
         ▼           │           │
    ✅ CHECKED_IN    │           │
         │      [Check-in]       │
         │           ▼           │
         │      ✅ CHECKED_IN    │
         │           │      [Check-in]
         │           │           ▼
         │           │      ✅ CHECKED_IN
         │           │           │
         └───────────┴───────────┤
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  Tài xế giao    │
                        │  cuối cùng      │
                        │ (Từ Kho C)      │
                        └────────┬────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │  📦 DELIVERED   │
                        │  Khách hàng     │
                        └─────────────────┘
```

---

## 🔄 API Endpoints Multi-Warehouse

### Check-in Lô Hàng
```
POST /api/warehouse-checkin/<tracking_id>/
Content-Type: application/x-www-form-urlencoded

Parameters:
- notes: Tình trạng hàng hóa (ví dụ: "Nguyên vẹn, đầy đủ")

Response:
{
  "success": true,
  "message": "Lô hàng LOG-2026-0001 đã được check-in",
  "tracking_id": 1
}
```

---

## 📝 Quy Tắc Sử Dụng

### Thêm Phương Tiện & Kho Mới
- Khi có người muốn hợp tác mới:
  1. Vào **Quản lý Phương tiện** → **+ Thêm phương tiện**
  2. Vào **Quản lý Kho bãi** → **+ Thêm kho bãi**
  3. Không giới hạn số lượng (khác với giới hạn 10)

### Check-in Đơn Hàng Tại Kho
1. Kho quản lý nhân viên vào **Quản lý Kho → Chi tiết kho**
2. Tab **"Đơn hàng chờ đến"** hiển thị lô hàng incoming
3. Nhấn **"Check-in"** → Kiểm tra hàng → Ghi chú → Xác nhận
4. Hệ thống tự động:
   - Gửi log về admin tổng
   - Chuyển lô sang kho tiếp theo
   - Cập nhật tracking real-time

### Theo Dõi Từ Admin Tổng
1. Vào **Quản lý → Tracking đơn hàng**
2. Xem **tất cả** check-in từ các kho khác
3. Nhấn **"Chi tiết"** để xem full lộ trình
4. Lịch sử tracking hiển thị:
   - Thời gian check-in
   - Kho nào check-in
   - Ai check-in
   - Ghi chú tình trạng

---

## 💡 Tips & Tricks

1. **Search nhanh**: Dùng search bar tại mỗi danh sách để tìm theo mã đơn, tên tài xế, kho
2. **Filter trạng thái**: Dùng dropdown filter để lọc đơn hàng theo trạng thái
3. **Xem timeline**: Trên trang chi tiết lộ trình, timeline hiển thị trực quan lô hàng đi qua kho nào
4. **Ghi chú chi tiết**: Khi check-in, hãy ghi chú rõ tình trạng hàng hóa để tracking đầy đủ
5. **Báo cáo**: Tất cả check-in đều được lưu log, admin có thể truy cập để kiểm tra

---

## ❓ Câu Hỏi Thường Gặp

**Q: Nếu muốn thêm kho hoặc phương tiện mới?**
A: Vào **Quản lý → Quản lý Kho bãi/Phương tiện** → Nút **"+ Thêm"**. Không có giới hạn số lượng.

**Q: Làm thế nào để check-in đơn hàng?**
A: Vào **Quản lý → Tracking đơn hàng** → Nhấn **"Check-in"** hoặc vào **Chi tiết kho → Đơn chờ → Check-in**

**Q: Ai có thể check-in lô hàng?**
A: Bất kỳ admin nào. Thời gian check-in sẽ được ghi lại cùng tên người check-in.

**Q: Nếu check-in sai, có thể hoàn tác không?**
A: Hiện tại không thể hoàn tác. Hãy kiểm tra kỹ trước khi xác nhận.

---

## 📞 Support
Nếu có lỗi hoặc câu hỏi, vui lòng liên hệ admin tổng (admin123).

**Created**: April 2026
**Version**: 1.0
