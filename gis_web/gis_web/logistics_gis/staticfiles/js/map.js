document.addEventListener("DOMContentLoaded", function () {
  // Initialize map centered on Vietnam (Ho Chi Minh City)
  var map = L.map("map").setView([10.762622, 106.660172], 10);

  // Add OpenStreetMap tiles with custom styling
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
    maxZoom: 18,
    minZoom: 1,
  }).addTo(map);

  // Custom icon for warehouses
  var warehouseIcon = L.divIcon({
    className: "custom-marker",
    html: '<div style="background: #f0b429;"></div>',
    iconSize: [30, 30],
    iconAnchor: [15, 30],
  });

  // Custom icon for vehicles
  var vehicleIcon = L.divIcon({
    className: "custom-marker",
    html: '<div style="background: #007bff;"></div>',
    iconSize: [30, 30],
    iconAnchor: [15, 30],
  });

  // Custom icon for orders
  var orderIcon = L.divIcon({
    className: "custom-marker",
    html: '<div style="background: #28a745;"></div>',
    iconSize: [30, 30],
    iconAnchor: [15, 30],
  });

  // Add warehouses (sample data)
  var warehouses = [
    { name: "Warehouse 1", lat: 10.762622, lng: 106.660172 },
    { name: "Warehouse 2", lat: 10.752622, lng: 106.650172 },
  ];
  warehouses.forEach(function (w) {
    L.marker([w.lat, w.lng], { icon: warehouseIcon })
      .addTo(map)
      .bindPopup(
        "<b><i class='fas fa-warehouse me-1'></i>" +
          w.name +
          "</b><br>Warehouse Location",
      );
  });

  // Add vehicles (sample data)
  var vehicles = [
    { name: "Vehicle 1", lat: 10.772622, lng: 106.670172 },
    { name: "Vehicle 2", lat: 10.742622, lng: 106.640172 },
  ];
  vehicles.forEach(function (v) {
    L.marker([v.lat, v.lng], { icon: vehicleIcon })
      .addTo(map)
      .bindPopup(
        "<b><i class='fas fa-truck me-1'></i>" +
          v.name +
          "</b><br>Vehicle Location",
      );
  });

  // Load approved orders from API with loading animation
  var loadingDiv = document.createElement("div");
  loadingDiv.className = "loading";
  loadingDiv.style.position = "absolute";
  loadingDiv.style.top = "50%";
  loadingDiv.style.left = "50%";
  loadingDiv.style.transform = "translate(-50%, -50%)";
  loadingDiv.style.zIndex = "1000";
  document.getElementById("map").appendChild(loadingDiv);

  fetch("/api/orders/")
    .then((response) => response.json())
    .then((data) => {
      // Remove loading
      if (loadingDiv.parentNode) {
        loadingDiv.parentNode.removeChild(loadingDiv);
      }

      data.forEach(function (order, index) {
        // Add marker with animation delay
        setTimeout(function () {
          var marker = L.marker([order.lat, order.lng], { icon: orderIcon })
            .addTo(map)
            .bindPopup(
              "<b><i class='fas fa-box me-1'></i>Mã đơn: " +
                order.code +
                "</b><br><i class='fas fa-user me-1'></i>Tên khách: " +
                order.customer_name,
            );

          // Animate marker appearance
          marker.setOpacity(0);
          marker.setOpacity(1);
        }, index * 100); // Stagger animation
      });
    })
    .catch((error) => {
      console.error("Error fetching orders:", error);
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
  `;
  document.head.appendChild(style);
});
