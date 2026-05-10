// Waypoint Routes
const express = require('express');
const router = express.Router();
const { verifyToken } = require('../middleware/auth');
const { checkRole, ROLES } = require('../middleware/rbac');
const waypointController = require('../controllers/waypointController');

// Mark shipment as arrived at warehouse
router.post('/:id/arrive', verifyToken, checkRole(ROLES.WAREHOUSE_ADMIN), waypointController.markArrived);

// Confirm shipment at warehouse (with photos/notes)
router.post('/:id/confirm', verifyToken, checkRole(ROLES.WAREHOUSE_ADMIN), waypointController.confirmShipment);

// Mark shipment as departed from warehouse
router.post('/:id/depart', verifyToken, checkRole(ROLES.WAREHOUSE_ADMIN), waypointController.markDeparted);

// Get waypoint details
router.get('/:id', verifyToken, waypointController.getWaypoint);

// Get checkpoint logs for waypoint
router.get('/:id/logs', verifyToken, waypointController.getCheckpointLogs);

module.exports = router;
