CREATE DATABASE IF NOT EXISTS logistics_gis;

\c logistics_gis;

CREATE TABLE IF NOT EXISTS admins (
  id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'warehouse_admin',
  warehouse_id INT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS warehouses (
  id SERIAL PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  location VARCHAR(255) NOT NULL,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  admin_id INT REFERENCES admins(id),
  type VARCHAR(50) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS shipments (
  id SERIAL PRIMARY KEY,
  origin_warehouse_id INT NOT NULL REFERENCES warehouses(id),
  destination_warehouse_id INT NOT NULL REFERENCES warehouses(id),
  status VARCHAR(50) DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS shipment_waypoints (
  id SERIAL PRIMARY KEY,
  shipment_id INT NOT NULL REFERENCES shipments(id),
  warehouse_id INT NOT NULL REFERENCES warehouses(id),
  order_index INT NOT NULL,
  status VARCHAR(50) DEFAULT 'pending',
  arrived_at TIMESTAMP,
  confirmed_at TIMESTAMP,
  confirmed_by INT REFERENCES admins(id),
  departed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS shipment_items (
  id SERIAL PRIMARY KEY,
  shipment_id INT NOT NULL REFERENCES shipments(id),
  product_name VARCHAR(150) NOT NULL,
  quantity INT NOT NULL,
  weight DECIMAL(10, 2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS checkpoint_logs (
  id SERIAL PRIMARY KEY,
  waypoint_id INT NOT NULL REFERENCES shipment_waypoints(id),
  action VARCHAR(50) NOT NULL,
  admin_id INT NOT NULL REFERENCES admins(id),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  notes TEXT,
  photos TEXT[] DEFAULT ARRAY[]::TEXT[]
);

CREATE INDEX idx_shipments_status ON shipments(status);
CREATE INDEX idx_shipment_waypoints_shipment_id ON shipment_waypoints(shipment_id);
CREATE INDEX idx_shipment_waypoints_warehouse_id ON shipment_waypoints(warehouse_id);
CREATE INDEX idx_checkpoint_logs_waypoint_id ON checkpoint_logs(waypoint_id);

-- Insert test data
INSERT INTO admins (username, email, password_hash, role) 
VALUES ('admin123', 'admin@test.com', '$2a$10$ZIH6WeYV.GbVhm8ZXE3hWuR.0dEcx7Q.UcDsZJwVN.IYrCWe9Mv0i', 'super_admin')
ON CONFLICT (username) DO NOTHING;

INSERT INTO warehouses (name, location, latitude, longitude, type)
VALUES 
  ('Warehouse A', 'Ha Noi', 21.0285, 105.8542, 'origin'),
  ('Warehouse B', 'Ha Nam', 20.5416, 105.6854, 'transit'),
  ('Warehouse C', 'Ha Noi', 21.0892, 105.8845, 'distribution')
ON CONFLICT DO NOTHING;
