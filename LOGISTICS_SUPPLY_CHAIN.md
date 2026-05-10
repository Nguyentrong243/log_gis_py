# Hệ Thống Quản Lý Chuỗi Cung Ứng Logistics

## 📋 Project Structure

```
supply-chain-logistics/
├── backend/
│   ├── config/
│   │   ├── database.js          # PostgreSQL config
│   │   ├── auth.js              # JWT config
│   │   └── constants.js
│   ├── middleware/
│   │   ├── auth.js              # JWT verification
│   │   ├── rbac.js              # Role-based access
│   │   └── errorHandler.js
│   ├── models/
│   │   ├── User.js
│   │   ├── Warehouse.js
│   │   ├── Shipment.js
│   │   ├── ShipmentWaypoint.js
│   │   ├── ShipmentItem.js
│   │   └── CheckpointLog.js
│   ├── routes/
│   │   ├── auth.js
│   │   ├── shipments.js
│   │   ├── waypoints.js
│   │   ├── warehouses.js
│   │   ├── admin.js
│   │   └── tracking.js
│   ├── controllers/
│   │   ├── authController.js
│   │   ├── shipmentController.js
│   │   ├── waypointController.js
│   │   ├── warehouseController.js
│   │   ├── adminController.js
│   │   └── trackingController.js
│   ├── services/
│   │   ├── shipmentService.js
│   │   ├── waypointService.js
│   │   ├── notificationService.js
│   │   └── reportService.js
│   ├── socket/
│   │   └── socketHandler.js
│   ├── migrations/
│   │   └── 001_initial_schema.sql
│   ├── seeds/
│   │   └── seedData.js
│   ├── app.js
│   ├── server.js
│   ├── .env.example
│   └── package.json
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Auth/
│   │   │   │   ├── Login.jsx
│   │   │   │   └── Register.jsx
│   │   │   ├── Dashboard/
│   │   │   │   ├── AdminDashboard.jsx
│   │   │   │   └── WarehouseDashboard.jsx
│   │   │   ├── Shipments/
│   │   │   │   ├── ShipmentList.jsx
│   │   │   │   ├── ShipmentDetail.jsx
│   │   │   │   ├── ShipmentCreate.jsx
│   │   │   │   ├── TrackingTimeline.jsx
│   │   │   │   └── ShipmentMap.jsx
│   │   │   ├── Warehouses/
│   │   │   │   ├── WarehouseList.jsx
│   │   │   │   ├── WarehouseDetail.jsx
│   │   │   │   └── WarehouseAdmin.jsx
│   │   │   ├── Common/
│   │   │   │   ├── Navbar.jsx
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   └── StatusBadge.jsx
│   │   │   └── Reports/
│   │   │       ├── DelayReport.jsx
│   │   │       └── PerformanceReport.jsx
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Shipments.jsx
│   │   │   ├── Tracking.jsx
│   │   │   ├── Warehouses.jsx
│   │   │   └── Reports.jsx
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── socketService.js
│   │   │   └── authService.js
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   ├── useShipment.js
│   │   │   └── useSocket.js
│   │   ├── utils/
│   │   │   ├── constants.js
│   │   │   ├── formatters.js
│   │   │   └── validators.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── .env.example
│   └── package.json
│
└── README.md
```

## 🗄️ Database Schema

### Users Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  username VARCHAR(100) UNIQUE NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role ENUM('super_admin', 'warehouse_admin', 'viewer'),
  warehouse_id UUID REFERENCES warehouses(id) ON DELETE SET NULL,
  full_name VARCHAR(255),
  phone VARCHAR(20),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Warehouses Table
```sql
CREATE TABLE warehouses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  location POINT NOT NULL,
  latitude DECIMAL(9, 6) NOT NULL,
  longitude DECIMAL(9, 6) NOT NULL,
  type ENUM('origin', 'transit', 'distribution', 'final') NOT NULL,
  address TEXT,
  admin_id UUID REFERENCES users(id),
  capacity INTEGER,
  contact_person VARCHAR(255),
  contact_phone VARCHAR(20),
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Shipments Table
```sql
CREATE TABLE shipments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  reference_code VARCHAR(50) UNIQUE NOT NULL,
  origin_warehouse_id UUID NOT NULL REFERENCES warehouses(id),
  destination_warehouse_id UUID NOT NULL REFERENCES warehouses(id),
  status ENUM('pending', 'in_transit', 'arrived', 'delayed', 'completed', 'cancelled') DEFAULT 'pending',
  total_weight DECIMAL(10, 2),
  total_items INTEGER,
  estimated_arrival TIMESTAMP,
  actual_arrival TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Shipment Waypoints Table
```sql
CREATE TABLE shipment_waypoints (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  shipment_id UUID NOT NULL REFERENCES shipments(id) ON DELETE CASCADE,
  warehouse_id UUID NOT NULL REFERENCES warehouses(id),
  order_index INTEGER NOT NULL,
  status ENUM('pending', 'arrived', 'confirmed', 'departed', 'failed') DEFAULT 'pending',
  estimated_arrival TIMESTAMP,
  actual_arrival TIMESTAMP,
  confirmed_at TIMESTAMP,
  confirmed_by UUID REFERENCES users(id),
  departed_at TIMESTAMP,
  notes TEXT,
  UNIQUE(shipment_id, warehouse_id, order_index)
);
```

### Shipment Items Table
```sql
CREATE TABLE shipment_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  shipment_id UUID NOT NULL REFERENCES shipments(id) ON DELETE CASCADE,
  product_name VARCHAR(255) NOT NULL,
  sku VARCHAR(100),
  quantity INTEGER NOT NULL,
  weight DECIMAL(10, 2),
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Checkpoint Logs Table
```sql
CREATE TABLE checkpoint_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  waypoint_id UUID NOT NULL REFERENCES shipment_waypoints(id) ON DELETE CASCADE,
  action ENUM('arrived', 'confirmed', 'departed', 'issue_raised', 'issue_resolved') NOT NULL,
  admin_id UUID NOT NULL REFERENCES users(id),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  notes TEXT,
  photos_url TEXT[],
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔐 Authentication Flow

1. User registers/logs in
2. Backend validates credentials
3. Backend generates JWT token (expires in 24h)
4. Frontend stores token in localStorage
5. Each request includes Authorization header
6. Middleware verifies token
7. User role checked for endpoint access

## 👥 Role-Based Access Control

### Super Admin
- ✅ Full system access
- ✅ View all shipments
- ✅ View all warehouses
- ✅ Manage all admins
- ✅ Generate reports
- ✅ Dashboard analytics

### Warehouse Admin
- ✅ View shipments for their warehouse
- ✅ Arrive/Confirm/Depart shipments
- ✅ View own warehouse details
- ✅ View checkpoint history
- ❌ Access other warehouses
- ❌ Manage users

### Viewer
- ✅ View only tracking information
- ✅ View read-only reports
- ❌ Modify shipments
- ❌ Access admin functions

## 📡 Real-time Features (Socket.io)

- Emit when shipment status changes
- Emit when waypoint updates
- Broadcast to relevant admins
- Live tracking updates
- Notification system

## 🗺️ Maps Integration

- Google Maps for route visualization
- Leaflet as alternative
- Markers for warehouses
- Polyline for route
- Info windows for details
- Live location updates

## 🎯 Status Flow

```
pending → in_transit → arrived → confirmed → departed → (repeat) → completed
                    ↓
                 delayed (if time exceeded)
                    ↓
                resolved/completed
```

## ⚡ Key Features Implementation

### 1. Shipment Creation
- Define origin & destination
- Add waypoints (intermediate warehouses)
- Add items (products, quantities, weights)
- Auto-calculate route
- Generate reference code

### 2. Waypoint Management
- Arrive: Mark package received at warehouse
- Confirm: Verify contents, upload photos, add notes
- Depart: Release to next destination
- Track time at each location

### 3. Dashboard Analytics
- Total shipments, on-time, delayed counts
- Average processing time per warehouse
- Bottleneck identification
- Performance metrics

### 4. Reports & Export
- Delay reports with reasons
- Performance metrics by warehouse
- Timeline analysis
- Export to Excel/PDF

## 🔧 Environment Variables

```env
# Backend
DATABASE_URL=postgresql://user:password@localhost:5432/supply_chain
JWT_SECRET=your_jwt_secret_key_here
JWT_EXPIRE=24h
NODE_ENV=development
PORT=3001

# Socket.io
SOCKET_URL=http://localhost:3001

# Google Maps (optional)
GOOGLE_MAPS_API_KEY=your_api_key

# Frontend
VITE_API_URL=http://localhost:3001/api
VITE_SOCKET_URL=http://localhost:3001
```

## 📦 Installation & Setup

### Backend
```bash
cd backend
npm install
npm run migrate
npm run seed
npm start
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Visit: http://localhost:5173

## 🧪 Test Credentials

- Super Admin: admin / admin123
- Warehouse Admin (HCM): warehouse_hcm / pass123
- Warehouse Admin (HN): warehouse_hn / pass123

## 📚 API Documentation

All endpoints require JWT token in Authorization header:
```
Authorization: Bearer {token}
```

### Public Endpoints
- POST /api/auth/register
- POST /api/auth/login
- GET /api/auth/verify

### Protected Endpoints (All roles)
- GET /api/shipments/:id/tracking - Public tracking view
- GET /api/warehouses/:id - Warehouse details

### Warehouse Admin Endpoints
- GET /api/warehouse/:id/shipments - Incoming shipments
- POST /api/waypoints/:id/arrive
- POST /api/waypoints/:id/confirm
- POST /api/waypoints/:id/depart

### Super Admin Endpoints
- GET /api/admin/dashboard
- GET /api/admin/reports/delays
- GET /api/admin/reports/performance
- GET /api/warehouses - List all
- POST /api/warehouses - Create
- PUT /api/warehouses/:id - Update
- DELETE /api/warehouses/:id

## 🎨 UI Color Scheme

- **Pending**: Gray (#6B7280)
- **In Transit**: Yellow (#FBBF24)
- **Arrived**: Blue (#3B82F6)
- **Confirmed**: Green (#10B981)
- **Delayed**: Red (#EF4444)
- **Completed**: Green (#059669)

## 📱 Responsive Design

- Mobile: 320px
- Tablet: 768px
- Desktop: 1024px+

## 🔒 Security Measures

- Password hashing with bcrypt
- JWT token verification
- Role-based access control
- HTTPS only in production
- SQL injection prevention (parameterized queries)
- CORS configuration
- Rate limiting
- Input validation
