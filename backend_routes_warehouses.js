// Warehouse Routes
const express = require('express');
const router = express.Router();
const { verifyToken } = require('../middleware/auth');
const { checkRole, ROLES, checkWarehouse } = require('../middleware/rbac');
const warehouseController = require('../controllers/warehouseController');

// Get all warehouses
router.get('/', verifyToken, warehouseController.getWarehouses);

// Get warehouse by ID
router.get('/:id', verifyToken, warehouseController.getWarehouseById);

// Create warehouse (Super Admin only)
router.post('/', verifyToken, checkRole(ROLES.SUPER_ADMIN), warehouseController.createWarehouse);

// Update warehouse
router.put('/:id', verifyToken, checkRole(ROLES.SUPER_ADMIN), warehouseController.updateWarehouse);

// Delete warehouse
router.delete('/:id', verifyToken, checkRole(ROLES.SUPER_ADMIN), warehouseController.deleteWarehouse);

// Get warehouse statistics
router.get('/:id/stats', verifyToken, checkWarehouse, warehouseController.getWarehouseStats);

// Get incoming shipments for warehouse
router.get('/:id/incoming', verifyToken, checkWarehouse, warehouseController.getIncomingShipments);

module.exports = router;
