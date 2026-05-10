# ⚡ QUICK FIX STEPS

## 🔴 Problem (Vấn Đề)
- Đăng nhập được nhưng vào dashboard không được
- Hiển thị lỗi: "Bạn không có quyền truy cập trang này"

## 🟢 Solution (Giải Pháp)

### Fix Applied (Đã áp dụng):
```python
# Trước:
def admin_dashboard_unified(request):
    if not hasattr(request.user, 'role') or request.user.role != 'ADMIN':
        return redirect('home')

# Sau:
@login_required(login_url='login')  # ← Thêm này
def admin_dashboard_unified(request):
    if request.user.role != 'ADMIN':  # ← Đơn giản hóa
        return redirect('home')
```

---

## 🧪 Test Now (Kiểm Tra Ngay)

### **Step 1: Logout**
- Click profile icon → "Đăng Xuất"

### **Step 2: Login Again**
- URL: `http://localhost:8000/login/`
- Username: `admin123`
- Password: `admin123`
- Click "Đăng Nhập"

### **Step 3: Go to Dashboard**
- URL: `http://localhost:8000/admin-dashboard/`
- Should see 6 vehicles + 6 warehouses + 4 drivers + 3 orders

---

## ✅ If Success
- ✓ Dashboard loads
- ✓ See statistics (4 cards at top)
- ✓ Can see vehicles/warehouses/drivers/orders
- ✓ Can search and filter

## ❌ If Still Failed
Run diagnostic:
```bash
python test_dashboard_access.py
```

If output shows:
```
✓ Admin user found: admin123
✓ Role: ADMIN
✓ Can access /admin-dashboard/
```

Then issue is browser/session related → Clear cache (Ctrl+Shift+Delete)

---

## 🔧 Files Modified
1. `core/views_management.py` - Added decorator + fixed imports
2. `FIX_DASHBOARD.md` - This guide

## 📊 Status
- Server: ✅ Running on port 8000
- Admin User: ✅ admin123 with role ADMIN
- Database: ✅ Sample data present
- Code: ✅ Fixed and restarted

**Ready to test!** 🚀
