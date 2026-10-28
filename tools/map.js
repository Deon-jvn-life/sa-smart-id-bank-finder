/* Branch map. Leaflet 1.9.4 is self-hosted. Tiles are OpenStreetMap. The table stays the full list. */
(function () {
  var root = document.getElementById("branch-map");
  var dataEl = document.getElementById("branch-map-data");
  if (!root || !dataEl) return;
  var data;
  try { data = JSON.parse(dataEl.textContent); } catch (e) { return; }
  if (!data || !data.points || !data.points.length) return;

  var status = root.querySelector(".map-status");
  var canvas = root.querySelector(".map-canvas");
  if (!canvas) return;

  function setStatus(text) {
    if (status) status.textContent = text;
  }

  function loadLeaflet() {
    if (window.L) return Promise.resolve();
    return new Promise(function (resolve, reject) {
      var css = document.createElement("link");
      css.rel = "stylesheet";
      css.href = "/vendor/leaflet/leaflet.css";
      document.head.appendChild(css);
      var script = document.createElement("script");
      script.src = "/vendor/leaflet/leaflet.js";
      script.onload = function () { resolve(); };
      script.onerror = function () { reject(new Error("leaflet")); };
      document.head.appendChild(script);
    });
  }

  function draw() {
    canvas.hidden = false;
    var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var map = L.map(canvas, {
      scrollWheelZoom: false,
      keyboard: true,
      fadeAnimation: !reduce,
      zoomAnimation: !reduce,
      markerZoomAnimation: !reduce,
      attributionControl: true
    });
    map.dragging.disable();
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    if (L.Icon && L.Icon.Default) {
      L.Icon.Default.imagePath = "/vendor/leaflet/images/";
    }
    var bounds = [];
    data.points.forEach(function (pt) {
      if (typeof pt.lat !== "number" || typeof pt.lon !== "number") return;
      if (pt.lat < -35.5 || pt.lat > -21.5 || pt.lon < 16 || pt.lon > 33.5) return;
      var marker = L.marker([pt.lat, pt.lon], {
        alt: pt.name || "Branch",
        title: pt.name || "Branch",
        keyboard: true
      });
      var html = '<p class="map-pop-name"><strong>' + esc(pt.name || "Branch") + '</strong></p>'
        + '<p>' + esc(pt.address || "") + '</p>'
        + '<p><a href="' + esc(pt.directions || "#") + '" target="_blank" rel="noopener">Get directions<span class="vh"> (opens in a new tab)</span></a></p>';
      marker.bindPopup(html, { className: "map-pop", maxWidth: 320, autoPan: true });
      marker.addTo(map);
      bounds.push([pt.lat, pt.lon]);
    });
    if (!bounds.length) {
      setStatus("No placed branches to show. The table is the full list.");
      return;
    }
    if (bounds.length === 1) map.setView(bounds[0], 16);
    else map.fitBounds(bounds, { padding: [28, 28], maxZoom: 14 });
    map.invalidateSize();
    var use = document.createElement("button");
    use.type = "button";
    use.className = "map-use";
    use.textContent = "Use the map";
    root.insertBefore(use, canvas);
    setStatus("The map is loaded. Use the zoom buttons, or choose Use the map to zoom with the scroll wheel.");
    function activate() {
      if (root.classList.contains("is-active")) return;
      root.classList.add("is-active");
      map.dragging.enable();
      map.scrollWheelZoom.enable();
      use.setAttribute("aria-pressed", "true");
      use.textContent = "Scroll zoom is on";
      setStatus("Scroll zoom is on. Arrow keys move the map when it is focused. The table is still the full list.");
    }
    use.addEventListener("click", activate);
    canvas.addEventListener("click", function (ev) {
      if (ev.target.closest("a, button, .leaflet-control")) return;
      activate();
    });
    map.on("focus", function () { /* keyboard pan stays available; scroll zoom stays off until a click */ });
  }

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function start() {
    setStatus("Loading the map.");
    loadLeaflet().then(draw).catch(function () {
      setStatus("The map could not be loaded. The table is still the full list.");
    });
  }

  if (!("IntersectionObserver" in window)) {
    start();
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    for (var i = 0; i < entries.length; i++) {
      if (!entries[i].isIntersecting) continue;
      io.disconnect();
      start();
      break;
    }
  }, { rootMargin: "300px 0px" });
  io.observe(root);
})();
