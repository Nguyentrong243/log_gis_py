// Shipment Routes
const express = require('express');
const router = express.Router();
const { verifyToken } = require('../middleware/auth');
const { checkRole, ROLES } = require('../middleware/rbac');
const shipmentController = require('../controllers/shipmentController');

// Create new shipment (Super Admin only)
router.post('/', verifyToken, checkRole(ROLES.SUPER_ADMIN), shipmentController.createShipment);

// Get all shipments (filtered by role)
router.get('/', verifyToken, shipmentController.getShipments);

// Get shipment by ID
router.get('/:id', verifyToken, shipmentController.getShipmentById);

// Update shipment
router.put('/:id', verifyToken, checkRole(ROLES.SUPER_ADMIN), shipmentController.updateShipment);

// Delete shipment
router.delete('/:id', verifyToken, checkRole(ROLES.SUPER_ADMIN), shipmentController.deleteShipment);

// Get shipment tracking
router.get('/:id/tracking', shipmentController.getShipmentTracking);

// Get shipments by warehouse
router.get('/warehouse/:warehouseId', verifyToken, shipmentController.getShipmentsByWarehouse);

module.exports = router;
