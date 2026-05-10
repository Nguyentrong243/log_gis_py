// Shipment Controller
const pool = require('../config/database');
const { v4: uuidv4 } = require('uuid');

exports.createShipment = async (req, res) => {
  try {
    const { originWarehouseId, destinationWarehouseId, items, waypoints, estimatedArrival } = req.body;

    // Generate reference code
    const referenceCode = `SH-${Date.now()}-${Math.random().toString(36).substr(2, 9).toUpperCase()}`;

    // Calculate totals
    const totalWeight = items.reduce((sum, item) => sum + (item.weight || 0), 0);
    const totalItems = items.reduce((sum, item) => sum + item.quantity, 0);

    // Start transaction
    const client = await pool.connect();
    try {
      await client.query('BEGIN');

      // Create shipment
      const shipmentResult = await client.query(
        'INSERT INTO shipments (reference_code, origin_warehouse_id, destination_warehouse_id, total_weight, total_items, estimated_arrival, status) VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING *',
        [referenceCode, originWarehouseId, destinationWarehouseId, totalWeight, totalItems, estimatedArrival, 'pending']
      );

      const shipmentId = shipmentResult.rows[0].id;

      // Add items
      for (const item of items) {
        await client.query(
          'INSERT INTO shipment_items (shipment_id, product_name, sku, quantity, weight, description) VALUES ($1, $2, $3, $4, $5, $6)',
          [shipmentId, item.productName, item.sku, item.quantity, item.weight, item.description]
        );
      }

      // Add waypoints
      for (let i = 0; i < waypoints.length; i++) {
        await client.query(
          'INSERT INTO shipment_waypoints (shipment_id, warehouse_id, order_index, status, estimated_arrival) VALUES ($1, $2, $3, $4, $5)',
          [shipmentId, waypoints[i].warehouseId, i, 'pending', waypoints[i].estimatedArrival]
        );
      }

      await client.query('COMMIT');

      res.status(201).json({
        message: 'Shipment created successfully',
        shipment: shipmentResult.rows[0]
      });
    } catch (err) {
      await client.query('ROLLBACK');
      throw err;
    } finally {
      client.release();
    }
  } catch (err) {
    console.error('Create shipment error:', err);
    res.status(500).json({ error: 'Failed to create shipment' });
  }
};

exports.getShipments = async (req, res) => {
  try {
    const { status, warehouseId, limit = 50, offset = 0 } = req.query;

    let query = 'SELECT * FROM shipments WHERE 1=1';
    let params = [];

    if (status) {
      query += ' AND status = $' + (params.length + 1);
      params.push(status);
    }

    // Filter by warehouse if warehouse admin
    if (req.user.role === 'warehouse_admin' && req.user.warehouseId) {
      query += ' AND (origin_warehouse_id = $' + (params.length + 1) + ' OR destination_warehouse_id = $' + (params.length + 2) + ')';
      params.push(req.user.warehouseId, req.user.warehouseId);
    }

    query += ' ORDER BY created_at DESC LIMIT $' + (params.length + 1) + ' OFFSET $' + (params.length + 2);
    params.push(limit, offset);

    const result = await pool.query(query, params);

    res.json({
      shipments: result.rows,
      total: result.rows.length
    });
  } catch (err) {
    console.error('Get shipments error:', err);
    res.status(500).json({ error: 'Failed to fetch shipments' });
  }
};

exports.getShipmentById = async (req, res) => {
  try {
    const { id } = req.params;

    const result = await pool.query(
      'SELECT * FROM shipments WHERE id = $1',
      [id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Shipment not found' });
    }

    res.json({ shipment: result.rows[0] });
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch shipment' });
  }
};

exports.getShipmentTracking = async (req, res) => {
  try {
    const { id } = req.params;

    // Get shipment details
    const shipmentResult = await pool.query(
      'SELECT * FROM shipments WHERE id = $1',
      [id]
    );

    if (shipmentResult.rows.length === 0) {
      return res.status(404).json({ error: 'Shipment not found' });
    }

    // Get waypoints
    const waypointsResult = await pool.query(
      `SELECT sw.*, w.name as warehouse_name, w.latitude, w.longitude
       FROM shipment_waypoints sw
       JOIN warehouses w ON sw.warehouse_id = w.id
       WHERE sw.shipment_id = $1
       ORDER BY sw.order_index`,
      [id]
    );

    // Get items
    const itemsResult = await pool.query(
      'SELECT * FROM shipment_items WHERE shipment_id = $1',
      [id]
    );

    res.json({
      shipment: shipmentResult.rows[0],
      waypoints: waypointsResult.rows,
      items: itemsResult.rows
    });
  } catch (err) {
    console.error('Get tracking error:', err);
    res.status(500).json({ error: 'Failed to fetch tracking' });
  }
};

exports.getShipmentsByWarehouse = async (req, res) => {
  try {
    const { warehouseId } = req.params;
    const { status } = req.query;

    let query = `
      SELECT DISTINCT s.* FROM shipments s
      JOIN shipment_waypoints sw ON s.id = sw.shipment_id
      WHERE sw.warehouse_id = $1
    `;
    let params = [warehouseId];

    if (status) {
      query += ' AND sw.status = $' + (params.length + 1);
      params.push(status);
    }

    query += ' ORDER BY s.created_at DESC';

    const result = await pool.query(query, params);

    res.json({ shipments: result.rows });
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch warehouse shipments' });
  }
};

exports.updateShipment = async (req, res) => {
  try {
    const { id } = req.params;
    const { status } = req.body;

    const result = await pool.query(
      'UPDATE shipments SET status = $1, updated_at = CURRENT_TIMESTAMP WHERE id = $2 RETURNING *',
      [status, id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Shipment not found' });
    }

    res.json({ shipment: result.rows[0] });
  } catch (err) {
    res.status(500).json({ error: 'Failed to update shipment' });
  }
};

exports.deleteShipment = async (req, res) => {
  try {
    const { id } = req.params;

    const result = await pool.query(
      'DELETE FROM shipments WHERE id = $1 RETURNING *',
      [id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Shipment not found' });
    }

    res.json({ message: 'Shipment deleted' });
  } catch (err) {
    res.status(500).json({ error: 'Failed to delete shipment' });
  }
};
