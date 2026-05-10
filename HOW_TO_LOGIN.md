# Hướng Dẫn Đăng Nhập Dashboard

## 🔐 Tài Khoản Đăng Nhập

### Admin Account
```
Username: admin123
Password: admin123
```

### URL Dashboard
```
http://localhost:8000/admin-dashboard/
```

## 📋 Bước Thực Hiện

### 1. Truy Cập Login
- Vào http://localhost:8000/login/

### 2. Đăng Nhập Admin
- Username: **admin123**
- Password: **admin123**
- Bấm "Login"

### 3. Truy Cập Dashboard
- Sau khi đăng nhập thành công
- Vào http://localhost:8000/admin-dashboard/

## ✅ Nếu Dashboard Vẫn Không Vào

**Nguyên Nhân Có Thể:**
1. ❌ Chưa đăng nhập - Cần login trước
2. ❌ Sai tài khoản - Không phải admin role
3. ❌ Session expired - Logout và login lại
4. ❌ Cookie issue - Clear cache browser (Ctrl+Shift+Delete)

**Cách Kiểm Tra:**
- Bấm F12 (Developer Tools)
- Vào tab Network
- Xem request /admin-dashboard/
- Nếu response code 302 = Redirect (chưa login)
- Nếu response code 200 = OK (được vào)

## 🔍 Kiểm Tra Dữ Liệu Mẫu

Sau khi vào dashboard, bạn sẽ thấy:

✅ **Thống Kê:**
- 6 Phương Tiện
- 6 Kho Bãi
- 4 Tài Xế
- 3 Đơn Hàng

✅ **Tab Phương Tiện:**
- Xe Tải Nhỏ 01 (51A-12345)
- Xe Van 02 (51B-54321)
- Xe Tải Vừa 03 (51C-78901)
- Xe Tải Lớn 04 (51D-34567)

✅ **Tab Kho Bãi:**
- Kho TPHCM (Tân Phú)
- Kho Hải Dương (Chợ Mơi)
- Kho Hà Nội (Thanh Xuân)
- Kho Nam Định (Thành Phố)

✅ **Tab Tài Xế:**
- Nguyễn Văn A (driver001)
- Trần Thị B (driver002)
- Phạm Văn C (driver003)
- Vũ Thị D (driver004)

✅ **Tab Đơn Hàng:**
- LOG-2026-0001 (TPHCM → Nam Định)
- LOG-2026-0002 (TPHCM → Hà Nội - Đã giao)
- LOG-2026-0003 (TPHCM → Hà Nội - Chờ xử lý)

## 🎯 Test Features

### 1. Tìm Kiếm
- Tab Phương Tiện: Tìm "51A" hoặc "Nguyễn"
- Tab Kho: Tìm "TPHCM" hoặc "Thanh Xuân"
- Tab Tài Xế: Tìm "driver001"
- Tab Đơn: Tìm "LOG-2026-0001"

### 2. Tracking
- Click "Tracking" trên đơn hàng LOG-2026-0001
- Xem timeline: TPHCM → Hải Dương → Hà Nội → Nam Định
- Xem status: Kho TPHCM đã CHECKED_IN, kho khác PENDING

### 3. Multi-Tab
- Click các tab: "Tất Cả", "Chờ Xử Lý", "Đang Vận Chuyển", "Đã Giao"
- Dữ liệu sẽ lọc theo tab

## 📞 Support

Nếu lỗi:
1. Check console (F12)
2. Check terminal Django
3. Clear cache browser
4. Logout/Login lại

---

**Version:** 1.0  
**Last Updated:** 20/04/2026
