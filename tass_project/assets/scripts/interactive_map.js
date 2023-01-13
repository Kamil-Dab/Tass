import CustomMarker from "./helpers/custom_marker.js";
import generateGradient from './helpers/generate_gradient.js';

$( document ).ready(function() {
    var map = L.map('map', {scrollWheelZoom: true});
    map.setView([39.518, -99.843], 5);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);
    rankingHandler(map);
    searchHandler(map);
});

function rankingHandler(map) {
    createMarkersForRows(map, $("#top-city-table").find(".city-row"), "ranking-tab");
}

function searchHandler(map) {
    let markers = [];
    $("#city-search-btn").on("click", function() {
        $.ajax({
            url: "/api/city/",
            type: "GET",
            data: {
                'query': $("#city-search-input").val()
            },
            success: function(response){
                fillSearchTable(response);
                markers.forEach(marker => map.removeLayer(marker.marker));
                markers = createMarkersForRows(map, $("#search-city-table").find(".city-row"), "search-tab");
            }
        });
    });
    $("#city-search-clear-btn").on("click", function() {
        $("#search-city-table").find(".city-row").remove();
        markers.forEach(marker => map.removeLayer(marker.marker));
        markers = [];
    });
}

function fillSearchTable(data) {
    data.sort((a,b) => (a.rating > b.rating) ? 1 : -1);
    $("#search-city-table").find(".city-row").remove();
    data.forEach(function(city) {
        $("#search-city-table > tbody").append(
            `<tr class="city-row" data-lat="${city.lat}" data-lng="${city.lng}">
                <td class="city-name">${city.city}</td>
                <td class="city-population">${city.population}</td>
                <td class="city-rating">${city.rating}</td>
            </tr>`
        );
    });
}

function createMarkersForRows(map, rows, currentTab) {
    let markers = []
    let otherTab = currentTab === "ranking-tab" ? "search-tab" : "ranking-tab";
    let topCityColors = generateGradient('#ff9933', '#00ff99', $(rows).length);
    $(rows).each(function(i) {
        const color = '#' + topCityColors[i];
        $(this).css("background-color", color);
        const lat = $(this).attr("data-lat");
        const lng = $(this).attr("data-lng");
        const label = $(this).find(".city-name").text();
        const rating = $(this).find(".city-rating").text();
        const marker = new CustomMarker(lat, lng, label, color, rating);
        marker.marker.addTo(map);
        $("#" + otherTab).on("click", function() {
            map.removeLayer(marker.marker);
        })
        $("#" + currentTab).on("click", function() {
            map.addLayer(marker.marker);
        })
        marker.marker.on("mouseover", () => marker.marker.openPopup())
        marker.marker.on("mouseout", () => marker.marker.closePopup())
        $(this).on("mouseover", function() {
            $(this).css("background-color", "#6200ff");
            marker.changeColor("#6200ff");
            marker.marker.openPopup();
        })
        $(this).on("mouseout", function() {
            $(this).css("background-color", color);
            marker.changeColor(color);
            marker.marker.closePopup();
        })
        markers.push(marker);
    });
    return markers;
}
