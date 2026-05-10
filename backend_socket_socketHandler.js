// Socket.io Handler - Real-time Updates
module.exports = (io) => {
  const connectedUsers = new Map();

  io.on('connection', (socket) => {
    console.log(`✓ Client connected: ${socket.id}`);

    // User joins with their warehouse/role
    socket.on('user_join', (data) => {
      const { userId, role, warehouseId } = data;
      
      connectedUsers.set(socket.id, {
        userId,
        role,
        warehouseId,
        socketId: socket.id
      });

      // Join room based on role
      if (role === 'super_admin') {
        socket.join('admin');
      } else if (role === 'warehouse_admin' && warehouseId) {
        socket.join(`warehouse:${warehouseId}`);
      }

      console.log(`✓ User ${userId} joined with role ${role}`);
    });

    // Shipment status changed
    socket.on('shipment_status_changed', (data) => {
      const { shipmentId, newStatus, warehouseId } = data;

      // Broadcast to all admins
      io.to('admin').emit('shipment_update', {
        shipmentId,
        status: newStatus,
        timestamp: new Date().toISOString()
      });

      // Broadcast to warehouse admin
      if (warehouseId) {
        io.to(`warehouse:${warehouseId}`).emit('shipment_update', {
          shipmentId,
          status: newStatus,
          timestamp: new Date().toISOString()
        });
      }
    });

    // Waypoint arrival
    socket.on('waypoint_arrived', (data) => {
      const { waypointId, warehouseId, shipmentId } = data;

      io.to('admin').emit('waypoint_event', {
        event: 'arrived',
        waypointId,
        warehouseId,
        shipmentId,
        timestamp: new Date().toISOString()
      });

      io.to(`warehouse:${warehouseId}`).emit('waypoint_event', {
        event: 'arrived',
        waypointId,
        shipmentId,
        timestamp: new Date().toISOString()
      });
    });

    // Waypoint confirmed
    socket.on('waypoint_confirmed', (data) => {
      const { waypointId, warehouseId, shipmentId, photos } = data;

      io.to('admin').emit('waypoint_event', {
        event: 'confirmed',
        waypointId,
        warehouseId,
        shipmentId,
        photos,
        timestamp: new Date().toISOString()
      });

      io.to(`warehouse:${warehouseId}`).emit('waypoint_event', {
        event: 'confirmed',
        waypointId,
        shipmentId,
        timestamp: new Date().toISOString()
      });
    });

    // Waypoint departed
    socket.on('waypoint_departed', (data) => {
      const { waypointId, warehouseId, shipmentId, nextWarehouse } = data;

      io.to('admin').emit('waypoint_event', {
        event: 'departed',
        waypointId,
        warehouseId,
        shipmentId,
        nextWarehouse,
        timestamp: new Date().toISOString()
      });

      // Notify next warehouse
      if (nextWarehouse) {
        io.to(`warehouse:${nextWarehouse}`).emit('incoming_shipment', {
          shipmentId,
          warehouseId,
          timestamp: new Date().toISOString()
        });
      }
    });

    // Request tracking update
    socket.on('request_tracking', (data) => {
      const { shipmentId } = data;
      socket.emit('tracking_requested', { shipmentId });
    });

    // Delay alert
    socket.on('delay_alert', (data) => {
      const { shipmentId, waypointId, delayMinutes } = data;

      io.to('admin').emit('alert', {
        type: 'delay',
        shipmentId,
        waypointId,
        delayMinutes,
        timestamp: new Date().toISOString()
      });
    });

    socket.on('disconnect', () => {
      connectedUsers.delete(socket.id);
      console.log(`✗ Client disconnected: ${socket.id}`);
    });

    // Error handling
    socket.on('error', (error) => {
      console.error('Socket error:', error);
    });
  });

  // Broadcast functions
  return {
    notifyShipmentStatusChange: (shipmentId, newStatus, warehouseId) => {
      io.to('admin').emit('shipment_update', {
        shipmentId,
        status: newStatus,
        timestamp: new Date().toISOString()
      });

      if (warehouseId) {
        io.to(`warehouse:${warehouseId}`).emit('shipment_update', {
          shipmentId,
          status: newStatus
        });
      }
    },

    notifyWaypointEvent: (event, waypointId, warehouseId, shipmentId, additionalData = {}) => {
      const eventData = {
        event,
        waypointId,
        shipmentId,
        timestamp: new Date().toISOString(),
        ...additionalData
      };

      io.to('admin').emit('waypoint_event', eventData);
      io.to(`warehouse:${warehouseId}`).emit('waypoint_event', eventData);
    },

    notifyAlert: (type, data) => {
      io.to('admin').emit('alert', {
        type,
        timestamp: new Date().toISOString(),
        ...data
      });
    },

    getConnectedUsers: () => Array.from(connectedUsers.values())
  };
};
