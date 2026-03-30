document.addEventListener("DOMContentLoaded", function () {
  // Initialize world map for global view
  var map = L.map("map").setView([0, 0], 2);
  window.map = map;

  // Add OpenStreetMap tiles for global detail
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
    maxZoom: 18,
    minZoom: 1,
  }).addTo(map);

  // Custom icon for warehouses
  var warehouseIcon = L.divIcon({
    className: "custom-marker",
    html: '<i class="fas fa-warehouse" style="color: #f0b429; font-size: 24px;"></i>',
    iconSize: [30, 30],
    iconAnchor: [15, 30],
  });

  // Custom icon for vehicles (will be set per vehicle)
  var vehicleIcon;

  // Custom icon for orders
  var orderIcon = L.divIcon({
    className: "custom-marker",
    html: '<i class="fas fa-box" style="color: #28a745; font-size: 24px;"></i>',
    iconSize: [30, 30],
    iconAnchor: [15, 30],
  });

  // Loading indicator for map data
  var loadingDiv = document.createElement("div");
  loadingDiv.className = "loading";
  loadingDiv.style.position = "absolute";
  loadingDiv.style.top = "50%";
  loadingDiv.style.left = "50%";
  loadingDiv.style.transform = "translate(-50%, -50%)";
  loadingDiv.style.zIndex = "1000";
  loadingDiv.innerHTML = "<div class='spinner-border text-warning' role='status'><span class='visually-hidden'>Loading...</span></div>";
  document.getElementById("map").appendChild(loadingDiv);

  // Fetch data: warehouses, vehicles, and approved orders
  Promise.all([
    fetch('/api/warehouses/', { credentials: 'same-origin' }).then(response => {
      if (!response.ok) throw new Error('Warehouses API blocked: ' + response.status);
      return response.json();
    }),
    fetch('/api/vehicles/', { credentials: 'same-origin' }).then(response => {
      if (!response.ok) throw new Error('Vehicles API blocked: ' + response.status);
      return response.json();
    }),
    fetch('/api/orders/', { credentials: 'same-origin' }).then(response => {
      if (!response.ok) throw new Error('Orders API blocked: ' + response.status);
      return response.json();
    }),
  ])
    .then(([warehouses, vehicles, orders]) => {
      if (loadingDiv.parentNode) {
        loadingDiv.parentNode.removeChild(loadingDiv);
      }

      warehouses.forEach(function (w) {
        // Skip showing warehouses for users - they will see after placing order
        // L.marker([w.lat, w.lng], { icon: warehouseIcon })
        //   .addTo(map)
        //   .bindPopup("<b><i class='fas fa-warehouse me-1'></i>" + w.name + "</b><br>Warehouse");
      });

      vehicles.forEach(function (v) {
        // Only show available drivers (no current orders)
        if (v.status === 'ACTIVE') {
          // Set icon based on vehicle type
          if (v.vehicle_type && v.vehicle_type.includes('Xe Máy')) {
            vehicleIcon = L.divIcon({
              className: "custom-marker",
              html: '<i class="fas fa-motorcycle" style="color: #007bff; font-size: 24px;"></i>',
              iconSize: [30, 30],
              iconAnchor: [15, 30],
            });
          } else {
            vehicleIcon = L.divIcon({
              className: "custom-marker",
              html: '<i class="fas fa-car" style="color: #007bff; font-size: 24px;"></i>',
              iconSize: [30, 30],
              iconAnchor: [15, 30],
            });
          }
          
          L.marker([v.lat, v.lng], { icon: vehicleIcon })
            .addTo(map)
            .bindPopup(
              "<b><i class='fas fa-truck me-1'></i>" + v.name + "</b><br>Tài xế: " +
                (v.driver_name || 'Chưa rõ') +
                "<br>Biển số: " + (v.plate_number || 'N/A') +
                "<br>Loại: " + (v.vehicle_type || 'N/A') +
                "<br>Trạng thái: " + (v.status || 'N/A'),
            );
        }
      });

      orders.forEach(function (order) {
        var colorIcon = order.status === 'APPROVED' ? orderIcon : vehicleIcon;
        var assigned = order.assigned_vehicle_name ? order.assigned_vehicle_name + ' (' + (order.assigned_vehicle_plate || 'N/A') + ')' : 'Chưa gán';
        var desc = "<b><i class='fas fa-box me-1'></i>Mã đơn: " + order.code + "</b>";
        desc += "<br><i class='fas fa-user me-1'></i>Khách: " + order.customer_name;
        desc += "<br><i class='fas fa-map-marker-alt me-1'></i>Địa chỉ: " + (order.customer_address || 'Không có');
        desc += "<br><strong>Trạng thái:</strong> " + order.status;
        desc += "<br><strong>ETA:</strong> " + (order.estimated_eta || 'Đang chờ');
        desc += "<br><strong>Tài xế:</strong> " + assigned;

        L.marker([order.lat, order.lng], { icon: colorIcon })
          .addTo(map)
          .bindPopup(desc);

        // Render route from warehouse to customer for assigned orders
        if (order.route && order.route.length >= 2) {
          var latlngs = order.route.map(function (point) {
            return [point.lat, point.lng];
          });
          L.polyline(latlngs, { color: 'blue', weight: 4, opacity: 0.7, dashArray: '8, 6' }).addTo(map);

          // Optionally place markers on start/end points
          L.marker([order.route[0].lat, order.route[0].lng], { icon: warehouseIcon }).addTo(map).bindPopup('Kho: ' + order.route[0].name);
          L.marker([order.route[1].lat, order.route[1].lng], { icon: orderIcon }).addTo(map).bindPopup('Giao khách: ' + order.code);
        }
      });
    })
    .catch((error) => {
      console.error("Error fetching map-data:", error);
      if (loadingDiv.parentNode) {
        loadingDiv.parentNode.removeChild(loadingDiv);
      }
    });

  // For create order page, add click event with animation
  if (document.getElementById("orderForm")) {
    var currentMarker = null;

    map.on("click", function (e) {
      var lat = e.latlng.lat;
      var lng = e.latlng.lng;

      // Update form fields
      document.getElementById("id_lat").value = lat;
      document.getElementById("id_lng").value = lng;

      // Remove previous marker with animation
      if (currentMarker) {
        map.removeLayer(currentMarker);
      }

      // Add new marker with bounce animation
      currentMarker = L.marker([lat, lng], { icon: orderIcon })
        .addTo(map)
        .bindPopup(
          "<b><i class='fas fa-map-pin me-1'></i>Delivery Location</b><br>Lat: " +
            lat.toFixed(6) +
            "<br>Lng: " +
            lng.toFixed(6),
        )
        .openPopup();

      // Bounce animation
      var icon = currentMarker.getElement();
      if (icon) {
        icon.style.animation = "bounce 0.5s ease";
      }
    });
  }

  // Add bounce animation CSS
  var style = document.createElement("style");
  style.textContent = `
    @keyframes bounce {
      0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
      40% { transform: translateY(-10px); }
      60% { transform: translateY(-5px); }
    }
    .custom-marker {
      display: flex !important;
      align-items: center;
      justify-content: center;
      border-radius: 50%;
      background: white;
      box-shadow: 0 2px 5px rgba(0,0,0,0.2);
      width: 30px !important;
      height: 30px !important;
    }
  `;
  document.head.appendChild(style);
});
