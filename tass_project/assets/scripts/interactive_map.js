import CustomMarker from "./helpers/custom_marker.js";
import generateGradient from './helpers/generate_gradient.js';

$( document ).ready(function() {
    var map = L.map('map', {scrollWheelZoom: true});
    map.setView([39.518, -99.843], 5);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);
    rankingHnadler(map);
});

function rankingHnadler(map) {
    let topCityColors = generateGradient('#ff9933', '#00ff99', $("#top-city-table").find(".top-city-row").length);
    $("#top-city-table").find(".top-city-row").each(function(i) {
        let cityColor = '#' + topCityColors[i];
        $(this).css("background-color", cityColor);
        const lat = $(this).attr("data-lat");
        const lng = $(this).attr("data-lng");
        const label = $(this).find(".top-city-name").text();
        const marker = new CustomMarker(lat, lng, label, cityColor);
        marker.marker.addTo(map);
        marker.marker.on("mouseover", () => marker.marker.openPopup())
        marker.marker.on("mouseout", () => marker.marker.closePopup())
        $(this).on("mouseover", function() {
            $(this).css("background-color", "#6200ff");
            marker.changeColor("#6200ff");
            marker.marker.openPopup();
        })
        $(this).on("mouseout", function() {
            $(this).css("background-color", cityColor);
            marker.changeColor(cityColor);
            marker.marker.closePopup();
        })
    });
}