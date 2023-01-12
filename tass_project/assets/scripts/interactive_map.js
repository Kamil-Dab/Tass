$( document ).ready(function() {
    var map = L.map('map', {scrollWheelZoom: true});
    map.setView([39.518, -99.843], 5);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);
});
