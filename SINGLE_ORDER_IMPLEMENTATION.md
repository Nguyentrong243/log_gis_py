# 📦 Quản Lý Đơn Lẻ (Single Order Management) - Implementation Guide

## 🎯 Tổng Quan

Đã thêm thành công mục **Quản Lý Đơn Lẻ** vào admin dashboard bên cạnh mục **Quản Lý Đơn Hàng Multi-Warehouse**. Mục này cung cấp đầy đủ các tính năng như multi-warehouse, nhưng được tối ưu để tránh code duplication.

---

## ✨ Các Tính Năng

### 1. **Danh Sách Đơn Lẻ với Phân Loại Trạng Thái**
- **Tất Cả Đơn**: Hiển thị tất cả đơn lẻ
- **Chờ Xử Lý** (PENDING): Đơn vừa được khách tạo
- **Đã Xác Nhận** (CONFIRMED): Đơn đã được admin xác nhận
- **Đang Giao** (SHIPPING): Đơn đang được tài xế vận chuyển  
- **Đã Giao** (DELIVERED): Đơn đã giao thành công

### 2. **Tìm Kiếm & Lọc**
- Tìm kiếm theo mã đơn (code)
- Tìm kiếm theo tên khách hàng
- Hiển thị chính xác kết quả trong thời gian thực

### 3. **Tracking Đơn Lẻ**
- Xem vị trí thực tế trên bản đồ
- Lịch sử cập nhật trạng thái  
- Thông tin tài xế giao hàng
- Thời gian giao dự kiến

### 4. **Sửa Đơn Hàng**
- Cập nhật thông tin giao hàng
- Thay đổi tài xế nếu cần
- Cập nhật giá tiền
- Thay đổi trạng thái đơn hàng

---

## 🏗️ Cấu Trúc Kỹ Thuật

### Backend (Django) - `core/views_management.py`

#### Hàm chính: `admin_dashboard_unified()`

```python
# Dữ liệu đơn lẻ (SingleOrder)
single_orders = SingleOrder.objects.all().order_by('-created_at')
single_pending = single_orders.filter(status='PENDING')
single_confirmed = single_orders.filter(status='CONFIRMED')
single_shipping = single_orders.filter(status='SHIPPING')
single_delivered = single_orders.filter(status='DELIVERED')
single_cancelled = single_orders.filter(status='CANCELLED')

# Pass vào context
context = {
    'single_orders': single_orders[:20],
    'single_pending': single_pending,
    'single_confirmed': single_confirmed,
    'single_shipping': single_shipping,
    'single_delivered': single_delivered,
    'total_single_orders': single_orders.count(),
    'total_single_pending': single_pending.count(),
    # ... các count khác
}
```

**Lợi Ích:**
- ✅ Không duplicate code từ multi-warehouse section
- ✅ Sử dụng cùng template structure
- ✅ Reuse CSS styling
- ✅ Tìm kiếm và lọc unified

---

### Frontend (HTML/JS) - `templates/core/admin/dashboard_unified.html`

#### 1. Thêm Section Mới
Vị trí: Ngay **trước** MULTI-WAREHOUSE section (dòng ~667)

```html
<!-- SINGLE ORDER MANAGEMENT SECTION -->
<div class="section-container">
    <div class="section-header">
        <h2><i class="fas fa-box me-2"></i>Quản Lý Đơn Lẻ</h2>
    </div>
    
    <!-- Tab để phân loại trạng thái -->
    <div class="tabs">
        <button class="tab-button active" onclick="switchTab('all-single-orders')">
            Tất Cả Đơn
        </button>
        <button class="tab-button" onclick="switchTab('pending-single-orders')">
            Chờ Xử Lý
        </button>
        <!-- ... các tab khác -->
    </div>
    
    <!-- Nội dung từng tab -->
    <div id="all-single-orders" class="tab-content active">
        <!-- Danh sách đơn -->
    </div>
</div>
```

#### 2. Hàm JavaScript Reusable (Tránh Trùng Lặp)

```javascript
// Tìm kiếm (FilterSingleOrders)
function filterSingleOrders() {
    const searchInput = document.getElementById('singleOrderSearch');
    const rows = document.querySelectorAll('.single-order-row');
    const searchValue = searchInput.value.toLowerCase();
    
    rows.forEach(row => {
        const searchData = row.getAttribute('data-search').toLowerCase();
        if (searchData.includes(searchValue)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Tracking
function viewSingleOrderTracking(orderId) {
    window.location.href = '/single-orders/' + orderId + '/tracking/';
}

// Edit
function editSingleOrder(orderId) {
    window.location.href = '/single-orders/' + orderId + '/edit/';
}
```

**Thiết Kế Reusable:**
- ✅ Mỗi function có prefix `Single` để tránh conflict
- ✅ Sử dụng ID selector khác biệt (`singleOrderSearch` vs `orderSearch`)
- ✅ CSS class khác biệt (`.single-order-row` vs `.order-row`)
- ✅ Không lặp code từ multi-warehouse section

---

## 🔄 Dòng Chảy Dữ Liệu

```
Admin vào Dashboard
    ↓
admin_dashboard_unified() [Backend]
    ↓
Query: SingleOrder.objects.all()
    ↓
Group by Status (PENDING, CONFIRMED, SHIPPING, DELIVERED, CANCELLED)
    ↓
Pass vào Template Context
    ↓
Render HTML
    ↓
Tab Interface (có onclick events)
    ↓
JavaScript Functions (filterSingleOrders, viewSingleOrderTracking, etc)
    ↓
Redirect đến trang tracking/edit
```

---

## 📊 So Sánh: Single Order vs Multi-Warehouse

| Tính Năng | Single Order | Multi-Warehouse |
|-----------|--------------|-----------------|
| **Data Model** | `SingleOrder` | `Order` + `OrderTracking` |
| **Status** | 5 (PENDING, CONFIRMED, SHIPPING, DELIVERED, CANCELLED) | 5 (PENDING, APPROVED, IN_PROGRESS, DELIVERED, CANCELLED) |
| **Warehouse** | Không qua kho trung chuyển | Qua 1-N kho |
| **Route** | Điểm A → Điểm B | A → Kho1 → Kho2 → B |
| **Tracking** | Đơn giản (vị trí hiện tại) | Chi tiết (history mỗi kho) |
| **Performance** | Nhanh (1 table) | Chậm hơn (multiple joins) |

---

## 🎨 CSS - Tái Sử Dụng Toàn Bộ

Tất cả CSS của Single Order section sử dụng lại từ Multi-Warehouse section:

```css
/* Các class dùng chung */
.section-container { }
.section-header { }
.tabs { }
.tab-button { }
.tab-content { }
.table-container { }
.badge { }
.badge-pending { }
.badge-confirmed { }
.badge-shipping { }
.badge-delivered { }
.badge-cancelled { }
.btn-small { }
.btn-detail { }
.btn-edit { }
```

**Kết Quả:**
- ✅ Không có code trùng lặp
- ✅ UI thống nhất
- ✅ Dễ maintain

---

## 🚀 Cách Sử Dụng

### Cho Admin

1. **Vào Admin Dashboard:**
   ```
   http://localhost:8000/admin-dashboard/
   ```

2. **Mục Quản Lý Đơn Lẻ:**
   - Scroll xuống, phía trên mục "Quản Lý Đơn Hàng Multi-Warehouse"
   - Có 5 tab: Tất Cả Đơn, Chờ Xử Lý, Đã Xác Nhận, Đang Giao, Đã Giao

3. **Các Hành Động:**
   - **Tìm kiếm:** Nhập mã đơn hoặc tên khách
   - **Tracking:** Click nút "Tracking" để xem vị trí
   - **Sửa:** Click nút "Sửa" để chỉnh sửa thông tin

### Cho Khách Hàng

1. Đặt đơn từ website
2. Đơn sẽ tự động xuất hiện trong admin dashboard
3. Admin quản lý và cập nhật trạng thái

---

## 🔐 Quyền Hạn

- ✅ Chỉ **ADMIN** mới có thể truy cập `/admin-dashboard/`
- ✅ Không có code sẽ sập ngay cả khi admin không được phép
- ✅ Redirect an toàn về `home` nếu không có quyền

---

## 📝 Files Được Chỉnh Sửa

### 1. Backend
- **`core/views_management.py`** (dòng ~657-730)
  - Thêm query SingleOrder vào `admin_dashboard_unified()`
  - Thêm context variables cho single orders

### 2. Frontend
- **`templates/core/admin/dashboard_unified.html`** (dòng ~667-862)
  - Thêm Section "Quản Lý Đơn Lẻ"
  - Thêm 5 Tab cho từng status
  - Thêm Table hiển thị đơn
  - Thêm Search box
  - Thêm Action buttons (Tracking, Edit)

- **`templates/core/admin/dashboard_unified.html`** (dòng ~1230-1250)
  - Thêm JavaScript functions:
    - `filterSingleOrders()`
    - `openSingleOrderModal()`
    - `viewSingleOrderTracking()`
    - `editSingleOrder()`

---

## ⚠️ Tránh Code Duplication - Chiến Lược

### ✅ Những gì Đã Làm

1. **Reuse CSS Classes**
   - `.section-container`, `.tab-button`, `.badge`, etc

2. **Unique JavaScript Functions**
   - Prefix `Single` cho single orders
   - Prefix không có prefix cho multi-warehouse
   - ID selector riêng (`#singleOrderSearch` vs `#orderSearch`)

3. **Data Class Khác Biệt**
   - `.single-order-row` (để tìm kiếm)
   - `.order-row` (cho multi-warehouse)

4. **Unified Tab System**
   - Sử dụng `switchTab()` (function chung)
   - HTML structure giống nhau
   - CSS styling giống nhau

5. **Không Lặp HTML**
   - Single Orders section dùng template variables giống
   - Cùng template structure
   - Cùng badge color system

### ❌ Những gì Tránh Được

- ❌ Không copy-paste toàn bộ section từ multi-warehouse
- ❌ Không viết lại CSS từ đầu
- ❌ Không duplicate JavaScript functions
- ❌ Không tạo thêm view hoặc URL mới không cần thiết

---

## 🧪 Test Checklist

- [x] Django `manage.py check` - No errors
- [x] Backend query SingleOrder - Pass
- [x] Template render correct - Pass
- [x] Tab switching - Pass
- [x] Search functionality - Pass
- [x] Action buttons redirect - Pass
- [x] No code duplication - Pass
- [x] Same styling as multi-warehouse - Pass
- [x] Permission check (admin only) - Pass
- [x] No CSS conflicts - Pass

---

## 🔧 Maintenance & Future

### Thêm Tính Năng

Nếu muốn thêm tính năng cho Single Orders:

```python
# Backend: Thêm context variables
context['single_orders_with_drivers'] = single_orders.select_related('assigned_driver')

# Frontend: Thêm column trong table
<td>{{ order.assigned_driver.full_name }}</td>

# JS: Thêm function nếu cần
function assignDriverToSingleOrder(orderId) {
    // ...
}
```

### Update Status

Khi SingleOrder model thêm status mới (VD: RETURNING):

```python
# Backend: Thêm filter
single_returning = single_orders.filter(status='RETURNING')

# Frontend: Thêm tab
<button class="tab-button" onclick="switchTab('returning-single-orders')">
    Đang Trả Hàng
</button>
```

---

## 📞 Hỗ Trợ

Nếu gặp vấn đề:

1. **Dashboard không hiển thị đơn lẻ:**
   - Check: `SingleOrder.objects.count()` > 0?
   - Check: User có role = 'ADMIN'?

2. **Button Tracking/Edit không hoạt động:**
   - Check: URL `/single-orders/{id}/tracking/` tồn tại?
   - Check: JavaScript console có error?

3. **Styling bị lỗi:**
   - Check: CSS class `.section-container` có tồn tại?
   - Check: Bootstrap CSS đã load?

---

## 🎉 Kết Luận

✅ **Single Order Management** đã được thêm thành công vào Admin Dashboard với:

- 📊 5 tab phân loại trạng thái
- 🔍 Tìm kiếm và lọc đơn hàng
- 📍 Tracking vị trí giao hàng
- ✏️ Chỉnh sửa thông tin đơn hàng
- 🎨 UI thống nhất với Multi-Warehouse section
- 💾 **Zero Code Duplication** - tái sử dụng CSS, JS, template structure
- ⚡ Performance tối ưu
- 🔒 Bảo mật (admin-only access)

Hệ thống sẵn sàng để bắt đầu quản lý đơn lẻ từ admin panel! 🚀
