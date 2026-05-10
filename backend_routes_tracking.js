// Tracking Routes (Public)
const express = require('express');
const router = express.Router();
const trackingController = require('../controllers/trackingController');

// Public tracking - no auth required
router.get('/shipment/:referenceCode', trackingController.getPublicTracking);

// Get tracking timeline
router.get('/shipment/:id/timeline', trackingController.getTimeline);

// Get tracking map data
router.get('/shipment/:id/map-data', trackingController.getMapData);

module.exports = router;
