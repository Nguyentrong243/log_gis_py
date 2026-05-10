// Role-Based Access Control Middleware
const ROLES = {
  SUPER_ADMIN: 'super_admin',
  WAREHOUSE_ADMIN: 'warehouse_admin',
  VIEWER: 'viewer'
};

const checkRole = (...allowedRoles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    if (!allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Access denied' });
    }

    next();
  };
};

const checkWarehouse = (req, res, next) => {
  // Warehouse admin can only access their own warehouse
  if (req.user.role === ROLES.WAREHOUSE_ADMIN) {
    if (req.params.warehouseId !== req.user.warehouseId && req.user.warehouseId) {
      return res.status(403).json({ error: 'Access denied to other warehouses' });
    }
  }
  next();
};

module.exports = {
  checkRole,
  checkWarehouse,
  ROLES
};
