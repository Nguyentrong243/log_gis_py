# 🎯 Quick Reference - Admin Dashboard

## Truy Cập
- **URL:** `http://yourdomain/admin-dashboard/`
- **Yêu cầu:** Admin role

## 📊 Dashboard Statistics
| Metric | Display |
|--------|---------|
| 🚗 Phương Tiện | Tổng số xe hoạt động |
| 🏢 Kho Bãi | Tổng số kho liên kết |
| 👨 Tài Xế | Tổng số tài xế |
| 📦 Đơn Hàng | Tổng số đơn |

## 🔑 Thông Tin Hiển Thị

### Phương Tiện (Vehicles)
```
- Tên Xe
- Biển Số Xe
- Loại Xe
- Tên Tài Xế ⭐
- Tuổi Tài Xế ⭐
- CCCD ⭐
- Trạng Thái
```

### Kho Bãi (Warehouses)
```
- Tên Kho ⭐
- Địa Chỉ ⭐
- Quản Lý Kho ⭐
- Số Điện Thoại ⭐
- Tọa Độ GIS
```

### Tài Xế (Drivers)
```
- Tên Tài Xế ⭐
- Ngày Sinh ⭐
- Tuổi ⭐
- CCCD ⭐
- Số Điện Thoại ⭐
- Địa Chỉ ⭐
- Trạng Thái
```

### Đơn Hàng (Orders)
```
- Mã Đơn
- Tên Khách Hàng
- Điểm Nhận
- Điểm Giao
- Trạng Thái
- Kho Hiện Tại
```

## 🎬 Quy Trình Check-in

```
1. Xe tới kho bãi A
   ↓
2. Admin Kho A nhấn "Check-in"
   ↓
3. Nhập ghi chú (tùy chọn)
   ↓
4. Xác nhận
   ↓
5. Status: CHECKED_IN
   Log được tạo
   Xe được phép chuyển sang kho B
```

## 🔍 Tìm Kiếm

| Section | Tìm Kiếm Theo |
|---------|--------------|
| 🚗 Xe | Tên, Biển số, Tài xế |
| 🏢 Kho | Tên kho, Địa chỉ, Quản lý |
| 👨 Tài xế | Tên, Số ĐT, CCCD |
| 📦 Đơn | Mã đơn, Tên khách |

## ⚙️ Hành Động

### Phương Tiện
- 👁️ Xem chi tiết
- ✏️ Sửa
- 🗑️ Xóa
- ➕ Thêm mới

### Kho
- 👁️ Xem chi tiết
- ✏️ Sửa
- 🗑️ Xóa
- ➕ Thêm mới

### Tài Xế
- 👁️ Xem chi tiết
- ✏️ Sửa
- ➕ Thêm mới

### Đơn Hàng
- 🗺️ Xem Tracking
- ✏️ Sửa
- ✅ Check-in (tab riêng)

## 📍 Tracking Details

### Timeline
Hiển thị tất cả kho trong lộ trình:
- Sequence
- Tên kho
- Trạng thái
- Địa chỉ
- Quản lý kho
- Thời gian check-in
- Ghi chú

### Activity Log
```
Thời gian | Hành động | Kho | Người | Ghi chú
---------|----------|-----|-------|--------
14:30    | Check-in | Kho A | Admin123 | OK
15:45    | Transfer | Kho B | Admin456 | Rất tốt
```

## 💡 Mẹo & Tricks

1. **Thêm nhiều mục:**
   - Không giới hạn số lượng
   - Dùng nút "Thêm [Tên]" ở mỗi section

2. **Xem lộ trình:**
   - Click nút "Tracking" trên đơn hàng
   - Xem timeline đầy đủ + lịch sử

3. **Tìm nhanh:**
   - Dùng search box realtime
   - Không cần bấm "Tìm"

4. **Check-in:**
   - Vào tab "Check-in Kho Bãi"
   - Chỉ hiển thị những cái chờ check-in
   - Click nút "Check-in" để xác nhận

## 🎨 Giao Diện

| Element | Ý Nghĩa |
|---------|---------|
| 🟢 Badge Xanh | Hoạt động, Đã giao, Checked-in |
| 🟡 Badge Vàng | Chờ xử lý, Pending |
| 🔵 Badge Xanh Lơ | Đang vận chuyển |
| 🔴 Badge Đỏ | Inactive, Lỗi |

## 📱 Responsive
- ✅ Desktop (100%)
- ✅ Tablet (90%)
- ✅ Mobile (85%)

## 🔒 Bảo Mật
- ✅ Require login
- ✅ Require Admin role
- ✅ CSRF protection
- ✅ SQL injection safe

## 📊 Tabs Đơn Hàng

1. **Tất Cả Đơn** - Toàn bộ đơn hàng
2. **Chờ Xử Lý** - Status = PENDING
3. **Đang Vận Chuyển** - Status = IN_PROGRESS
4. **Đã Giao** - Status = DELIVERED

## 🚀 Keyboard Shortcuts
```
Ctrl+F: Tìm kiếm (browser)
Tab: Di chuyển focus
Enter: Xác nhận hành động
```

## ❓ FAQs

**Q: Không thấy phương tiện mới?**
A: Refresh trang (F5) hoặc clear cache

**Q: Check-in không hoạt động?**
A: Kiểm tra order có tracking, user có role admin

**Q: Xóa kho có ảnh hưởng?**
A: Có thể ảnh hưởng order nếu đã tham chiếu

**Q: Có thể thêm bao nhiêu kho/xe?**
A: Không giới hạn! Thêm bao nhiêu tùy thích

**Q: Tracking realtime?**
A: Cần refresh, hoặc có thể thêm WebSocket sau

## 📧 Support

Liên hệ: admin@yourdomain.com

---
**Last Updated:** 20/04/2026
