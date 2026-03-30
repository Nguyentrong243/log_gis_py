document.addEventListener("DOMContentLoaded", function () {
  // Initialize world map for global overview with detailed zoom
  var map = L.map("map").setView([0, 0], 2);

  // add OSM tiles for global map
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap contributors",
    maxZoom: 19,
  }).addTo(map);

  // Add scale and fullscreen control if available
  L.control.scale({ position: 'bottomleft', metric: true, imperial: false }).addTo(map);

  // Reset view button
  var resetView = L.Control.extend({
    options: { position: 'topleft' },
    onAdd: function () {
      var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
      container.style.backgroundColor = 'white';
      container.style.width = '32px';
      container.style.height = '32px';
      container.style.display = 'flex';
      container.style.alignItems = 'center';
      container.style.justifyContent = 'center';
      container.style.cursor = 'pointer';
      container.innerHTML = '<i class="fas fa-globe"></i>';
      container.title = 'Reset world view';
      container.onclick = function () {
        map.setView([0, 0], 2);
      };
      return container;
    },
  });
  map.addControl(new resetView());

  // Custom icons
  var warehouseIcon = L.divIcon({
    className: "custom-marker",
    html: '<i class="fas fa-warehouse" style="color: #f0b429; font-size: 24px;"></i>',
    iconSize: [30, 30],
    iconAnchor: [15, 30],
  });
  var orderIcon = L.divIcon({
    className: "custom-marker",
    html: '<i class="fas fa-box" style="color: #28a745; font-size: 24px;"></i>',
    iconSize: [30, 30],
    iconAnchor: [15, 30],
  });

  function addMarkers(layerData, icon, popupFn) {
    layerData.forEach(function (item) {
      L.marker([item.lat, item.lng], { icon: icon })
        .addTo(map)
        .bindPopup(popupFn(item));
    });
  }

  // add sample data quickly if empty DB for debug - but hide warehouses for users
  // var sampleWarehouses = [
  //   { name: "Warehouse A", lat: 10.762622, lng: 106.660172 },
  //   { name: "Warehouse B", lat: 51.507351, lng: -0.127758 },
  // ];
  // addMarkers(sampleWarehouses, warehouseIcon, function (w) { return "<b>" + w.name + "</b><br>Warehouse"; });

  // fetch vehicles 
  fetch('/api/vehicles/')
    .then(response => response.json())
    .then(data => {
      if (data.length > 0) {
        data.forEach(function (v) {
          // Only show available drivers
          if (v.status === 'ACTIVE') {
            // Set icon based on vehicle type
            var vehicleIcon;
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
              .bindPopup('<b>' + v.name + '</b><br>Driver: ' + (v.driver_name || 'N/A') + '<br>Plate: ' + (v.plate_number || 'N/A') + '<br>Status: ' + (v.status || 'N/A'));
          }
        });
      }
    }).catch(err => console.error('Error loading vehicles:', err));

  // fetch approved orders
  fetch('/api/orders/')
    .then(response => response.json())
    .then(data => {
      if (data.length > 0) {
        addMarkers(data, orderIcon, function (o) {
          return '<b>Order: ' + o.code + '</b><br>Customer: ' + o.customer_name + '<br>Address: ' + (o.customer_address || 'N/A') + '<br>Status: ' + o.status + '<br>ETA: ' + (o.estimated_eta || 'N/A');
        });
      }
    }).catch(err => console.error('Error loading orders:', err));

  // Click vào map để chọn tọa độ tạo đơn
  map.on('click', function(e) {
    var lat = e.latlng.lat.toFixed(6);
    var lng = e.latlng.lng.toFixed(6);

    // hiển thị input text
    var latDisplay = document.getElementById('lat_display');
    var lngDisplay = document.getElementById('lng_display');
    var latInput = document.getElementById('id_lat');
    var lngInput = document.getElementById('id_lng');

    if (latDisplay) latDisplay.value = lat;
    if (lngDisplay) lngDisplay.value = lng;
    if (latInput) latInput.value = lat;
    if (lngInput) lngInput.value = lng;

    L.marker([lat, lng]).addTo(map).bindPopup('Pickup location').openPopup();
  });

  // add zoom in/out instructions
  var info = L.control({ position: 'bottomright' });
  info.onAdd = function () {
    var div = L.DomUtil.create('div', 'info');
    div.innerHTML = '<h6>Map Controls</h6><p>Scroll để zoom, kéo thả để di chuyển.</p>';
    return div;
  };
  info.addTo(map);

  // Add CSS for custom markers
  var style = document.createElement("style");
  style.textContent = `
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
