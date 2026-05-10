// React: Shipment Tracking Component
import React, { useState, useEffect } from 'react';
import { shipmentAPI, trackingAPI } from '../services/api';
import socketService from '../services/socketService';
import StatusBadge, { StatusTimeline } from './StatusBadge';
import ShipmentMap from './ShipmentMap';

export const ShipmentDetail = ({ shipmentId }) => {
  const [shipment, setShipment] = useState(null);
  const [waypoints, setWaypoints] = useState([]);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchShipmentData();
    setupSocketListener();

    return () => {
      socketService.off('shipment_update');
      socketService.off('waypoint_event');
    };
  }, [shipmentId]);

  const fetchShipmentData = async () => {
    try {
      setLoading(true);
      const response = await shipmentAPI.getTracking(shipmentId);
      setShipment(response.data.shipment);
      setWaypoints(response.data.waypoints);
      setItems(response.data.items);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const setupSocketListener = () => {
    socketService.onShipmentUpdate((data) => {
      if (data.shipmentId === shipmentId) {
        fetchShipmentData();
      }
    });

    socketService.onWaypointEvent((data) => {
      const waypoint = waypoints.find((w) => w.id === data.waypointId);
      if (waypoint) {
        fetchShipmentData();
      }
    });
  };

  if (loading) {
    return <div className="text-center py-12">Đang tải...</div>;
  }

  if (error) {
    return <div className="text-red-500 p-4">Lỗi: {error}</div>;
  }

  if (!shipment) {
    return <div className="text-gray-500 p-4">Không tìm thấy lô hàng</div>;
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              {shipment.reference_code}
            </h1>
            <p className="text-gray-500 mt-1">
              Tạo: {new Date(shipment.created_at).toLocaleString('vi-VN')}
            </p>
          </div>
          <StatusBadge status={shipment.status} className="text-lg" />
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-4 mt-6">
          <div>
            <p className="text-sm text-gray-500">Tổng cân nặng</p>
            <p className="text-2xl font-bold text-gray-900">
              {shipment.total_weight}kg
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Số lượng</p>
            <p className="text-2xl font-bold text-gray-900">
              {shipment.total_items}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-500">Số kho trung gian</p>
            <p className="text-2xl font-bold text-gray-900">
              {waypoints.length}
            </p>
          </div>
        </div>
      </div>

      {/* Map */}
      <ShipmentMap waypoints={waypoints} />

      {/* Timeline */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-6">Lộ trình</h2>
        <StatusTimeline waypoints={waypoints} />
      </div>

      {/* Items */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Danh sách sản phẩm</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="px-4 py-2 text-left text-sm font-semibold">Tên sản phẩm</th>
                <th className="px-4 py-2 text-left text-sm font-semibold">SKU</th>
                <th className="px-4 py-2 text-left text-sm font-semibold">Số lượng</th>
                <th className="px-4 py-2 text-left text-sm font-semibold">Cân nặng</th>
              </tr>
            </thead>
            <tbody>
              {items.map((item) => (
                <tr key={item.id} className="border-b hover:bg-gray-50">
                  <td className="px-4 py-3">{item.product_name}</td>
                  <td className="px-4 py-3">{item.sku || '-'}</td>
                  <td className="px-4 py-3">{item.quantity}</td>
                  <td className="px-4 py-3">{item.weight || '-'}kg</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default ShipmentDetail;
