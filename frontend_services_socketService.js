// React: Socket.io Service
import io from 'socket.io-client';
import { useAuthStore } from '../stores/authStore';

let socket = null;

export const socketService = {
  connect: () => {
    const SOCKET_URL = import.meta.env.VITE_SOCKET_URL || 'http://localhost:3001';
    const { user, token } = useAuthStore.getState();

    socket = io(SOCKET_URL, {
      auth: { token },
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: 5
    });

    // Emit user join
    if (user) {
      socket.emit('user_join', {
        userId: user.id,
        role: user.role,
        warehouseId: user.warehouseId
      });
    }

    socket.on('connect', () => {
      console.log('✓ Socket connected');
    });

    socket.on('disconnect', () => {
      console.log('✗ Socket disconnected');
    });

    socket.on('error', (error) => {
      console.error('Socket error:', error);
    });

    return socket;
  },

  disconnect: () => {
    if (socket) {
      socket.disconnect();
    }
  },

  getSocket: () => socket,

  on: (event, callback) => {
    if (socket) {
      socket.on(event, callback);
    }
  },

  off: (event) => {
    if (socket) {
      socket.off(event);
    }
  },

  emit: (event, data) => {
    if (socket) {
      socket.emit(event, data);
    }
  },

  // Listen to shipment updates
  onShipmentUpdate: (callback) => {
    if (socket) {
      socket.on('shipment_update', callback);
    }
  },

  // Listen to waypoint events
  onWaypointEvent: (callback) => {
    if (socket) {
      socket.on('waypoint_event', callback);
    }
  },

  // Listen to alerts
  onAlert: (callback) => {
    if (socket) {
      socket.on('alert', callback);
    }
  },

  // Listen to incoming shipments
  onIncomingShipment: (callback) => {
    if (socket) {
      socket.on('incoming_shipment', callback);
    }
  }
};

export default socketService;
