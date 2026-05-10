// Admin Routes
const express = require('express');
const router = express.Router();
const { verifyToken } = require('../middleware/auth');
const { checkRole, ROLES } = require('../middleware/rbac');
const adminController = require('../controllers/adminController');

// Dashboard (Super Admin only)
router.get('/dashboard', verifyToken, checkRole(ROLES.SUPER_ADMIN), adminController.getDashboard);

// Reports
router.get('/reports/delays', verifyToken, checkRole(ROLES.SUPER_ADMIN), adminController.getDelayReport);
router.get('/reports/performance', verifyToken, checkRole(ROLES.SUPER_ADMIN), adminController.getPerformanceReport);
router.get('/reports/export', verifyToken, checkRole(ROLES.SUPER_ADMIN), adminController.exportReport);

// User management
router.get('/users', verifyToken, checkRole(ROLES.SUPER_ADMIN), adminController.getUsers);
router.post('/users', verifyToken, checkRole(ROLES.SUPER_ADMIN), adminController.createUser);
router.put('/users/:id', verifyToken, checkRole(ROLES.SUPER_ADMIN), adminController.updateUser);
router.delete('/users/:id', verifyToken, checkRole(ROLES.SUPER_ADMIN), adminController.deleteUser);

// Warehouse management
router.post('/warehouses', verifyToken, checkRole(ROLES.SUPER_ADMIN), adminController.createWarehouse);
router.put('/warehouses/:id', verifyToken, checkRole(ROLES.SUPER_ADMIN), adminController.updateWarehouse);
router.delete('/warehouses/:id', verifyToken, checkRole(ROLES.SUPER_ADMIN), adminController.deleteWarehouse);

module.exports = router;
