// Waypoint Controller
const pool = require('../config/database');

exports.markArrived = async (req, res) => {
  try {
    const { id } = req.params;

    // Update waypoint status
    const result = await pool.query(
      `UPDATE shipment_waypoints 
       SET status = 'arrived', actual_arrival = CURRENT_TIMESTAMP
       WHERE id = $1
       RETURNING *`,
      [id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Waypoint not found' });
    }

    const waypoint = result.rows[0];

    // Log checkpoint
    await pool.query(
      `INSERT INTO checkpoint_logs (waypoint_id, action, admin_id, timestamp)
       VALUES ($1, 'arrived', $2, CURRENT_TIMESTAMP)`,
      [id, req.user.userId]
    );

    res.json({
      message: 'Shipment marked as arrived',
      waypoint
    });
  } catch (err) {
    console.error('Mark arrived error:', err);
    res.status(500).json({ error: 'Failed to mark as arrived' });
  }
};

exports.confirmShipment = async (req, res) => {
  try {
    const { id } = req.params;
    const { notes, photos } = req.body;

    // Update waypoint status
    const result = await pool.query(
      `UPDATE shipment_waypoints 
       SET status = 'confirmed', confirmed_at = CURRENT_TIMESTAMP, confirmed_by = $1
       WHERE id = $2
       RETURNING *`,
      [req.user.userId, id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Waypoint not found' });
    }

    const waypoint = result.rows[0];

    // Log checkpoint with photos
    await pool.query(
      `INSERT INTO checkpoint_logs (waypoint_id, action, admin_id, timestamp, notes, photos_url)
       VALUES ($1, 'confirmed', $2, CURRENT_TIMESTAMP, $3, $4)`,
      [id, req.user.userId, notes, photos || []]
    );

    res.json({
      message: 'Shipment confirmed',
      waypoint
    });
  } catch (err) {
    console.error('Confirm shipment error:', err);
    res.status(500).json({ error: 'Failed to confirm shipment' });
  }
};

exports.markDeparted = async (req, res) => {
  try {
    const { id } = req.params;

    // Get waypoint to find shipment
    const waypointResult = await pool.query(
      'SELECT shipment_id FROM shipment_waypoints WHERE id = $1',
      [id]
    );

    if (waypointResult.rows.length === 0) {
      return res.status(404).json({ error: 'Waypoint not found' });
    }

    const shipmentId = waypointResult.rows[0].shipment_id;

    // Update waypoint status
    const result = await pool.query(
      `UPDATE shipment_waypoints 
       SET status = 'departed', departed_at = CURRENT_TIMESTAMP
       WHERE id = $1
       RETURNING *`,
      [id]
    );

    // Check if all waypoints are departed except the last
    const allWaypoints = await pool.query(
      `SELECT COUNT(*) as total, SUM(CASE WHEN status IN ('departed', 'confirmed') THEN 1 ELSE 0 END) as completed
       FROM shipment_waypoints
       WHERE shipment_id = $1`,
      [shipmentId]
    );

    const stats = allWaypoints.rows[0];
    const statusToUpdate = stats.completed >= stats.total - 1 ? 'completed' : 'in_transit';

    // Update shipment status
    await pool.query(
      'UPDATE shipments SET status = $1, updated_at = CURRENT_TIMESTAMP WHERE id = $2',
      [statusToUpdate, shipmentId]
    );

    // Log checkpoint
    await pool.query(
      `INSERT INTO checkpoint_logs (waypoint_id, action, admin_id, timestamp)
       VALUES ($1, 'departed', $2, CURRENT_TIMESTAMP)`,
      [id, req.user.userId]
    );

    res.json({
      message: 'Shipment marked as departed',
      waypoint: result.rows[0]
    });
  } catch (err) {
    console.error('Mark departed error:', err);
    res.status(500).json({ error: 'Failed to mark as departed' });
  }
};

exports.getWaypoint = async (req, res) => {
  try {
    const { id } = req.params;

    const result = await pool.query(
      `SELECT sw.*, w.name as warehouse_name, w.latitude, w.longitude
       FROM shipment_waypoints sw
       JOIN warehouses w ON sw.warehouse_id = w.id
       WHERE sw.id = $1`,
      [id]
    );

    if (result.rows.length === 0) {
      return res.status(404).json({ error: 'Waypoint not found' });
    }

    res.json({ waypoint: result.rows[0] });
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch waypoint' });
  }
};

exports.getCheckpointLogs = async (req, res) => {
  try {
    const { id } = req.params;

    const result = await pool.query(
      `SELECT cl.*, u.username as admin_username
       FROM checkpoint_logs cl
       LEFT JOIN users u ON cl.admin_id = u.id
       WHERE cl.waypoint_id = $1
       ORDER BY cl.timestamp DESC`,
      [id]
    );

    res.json({ logs: result.rows });
  } catch (err) {
    res.status(500).json({ error: 'Failed to fetch checkpoint logs' });
  }
};
