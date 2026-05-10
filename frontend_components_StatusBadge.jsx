// React: Status Badge Component
import React from 'react';

const STATUS_CONFIG = {
  pending: {
    bg: 'bg-gray-100',
    text: 'text-gray-800',
    badge: 'bg-gray-200',
    icon: '⏳',
    label: 'Chờ xử lý'
  },
  in_transit: {
    bg: 'bg-yellow-50',
    text: 'text-yellow-800',
    badge: 'bg-yellow-200',
    icon: '🚚',
    label: 'Đang vận chuyển'
  },
  arrived: {
    bg: 'bg-blue-50',
    text: 'text-blue-800',
    badge: 'bg-blue-200',
    icon: '📦',
    label: 'Đã đến'
  },
  confirmed: {
    bg: 'bg-green-50',
    text: 'text-green-800',
    badge: 'bg-green-200',
    icon: '✅',
    label: 'Đã xác nhận'
  },
  departed: {
    bg: 'bg-blue-50',
    text: 'text-blue-800',
    badge: 'bg-blue-200',
    icon: '➡️',
    label: 'Đã xuất kho'
  },
  completed: {
    bg: 'bg-emerald-50',
    text: 'text-emerald-800',
    badge: 'bg-emerald-200',
    icon: '🎉',
    label: 'Hoàn thành'
  },
  delayed: {
    bg: 'bg-red-50',
    text: 'text-red-800',
    badge: 'bg-red-200',
    icon: '⚠️',
    label: 'Chậm trễ'
  },
  cancelled: {
    bg: 'bg-red-50',
    text: 'text-red-800',
    badge: 'bg-red-200',
    icon: '❌',
    label: 'Hủy'
  }
};

export const StatusBadge = ({ status, className = '' }) => {
  const config = STATUS_CONFIG[status] || STATUS_CONFIG.pending;

  return (
    <span
      className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium ${config.badge} ${config.text} ${className}`}
    >
      <span>{config.icon}</span>
      {config.label}
    </span>
  );
};

export const StatusTimeline = ({ waypoints }) => {
  return (
    <div className="relative">
      {waypoints.map((waypoint, index) => (
        <div key={waypoint.id} className="flex gap-4 pb-8">
          {/* Timeline dot */}
          <div className="flex flex-col items-center">
            <div
              className={`w-4 h-4 rounded-full border-2 ${
                waypoint.status === 'completed' || waypoint.status === 'confirmed'
                  ? 'bg-green-500 border-green-500'
                  : waypoint.status === 'arrived'
                  ? 'bg-blue-500 border-blue-500'
                  : 'bg-gray-300 border-gray-300'
              }`}
            />
            {index < waypoints.length - 1 && (
              <div className="w-1 h-12 bg-gray-300 my-2" />
            )}
          </div>

          {/* Content */}
          <div className="flex-1">
            <div className="font-semibold text-gray-900">
              {waypoint.warehouse_name}
            </div>
            <div className="text-sm text-gray-500 mt-1">
              {waypoint.estimated_arrival ? (
                <>
                  Dự kiến: {new Date(waypoint.estimated_arrival).toLocaleString('vi-VN')}
                </>
              ) : (
                'Dự kiến: Chưa xác định'
              )}
            </div>
            {waypoint.actual_arrival && (
              <div className="text-sm text-gray-500">
                Đến thực tế: {new Date(waypoint.actual_arrival).toLocaleString('vi-VN')}
              </div>
            )}
            <div className="mt-2">
              <StatusBadge status={waypoint.status} />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};

export default StatusBadge;
