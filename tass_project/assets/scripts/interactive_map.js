import CustomMarker from "./helpers/custom_marker.js";
import generateGradient from './helpers/generate_gradient.js';
import numberFormatter from './helpers/number_formatter.js';

$( document ).ready(function() {
    setupRatingSlider();
    setupPopulationSlider();
    var map = L.map('map', {scrollWheelZoom: true});
    map.setView([39.518, -99.843], 5);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);
    rankingHandler(map);
    searchHandler(map);
    heatMapHandler(map);
});

function setupRatingSlider() {
    $("#rating-slider").slider({
        min: 0,
        max: 10,
        step: 0.1,
        values: [0, 10],
        slide: function(event, ui) {
            let output = $("#rating-output > span");
            let outputStr = ""
            let chosenValues = ui.values.sort((a,b) => {return (a - b)});
            if (chosenValues[0] < chosenValues[1]) {
                outputStr = chosenValues[0].toFixed(1) + " - " + chosenValues[1].toFixed(1);
            } else {
                outputStr = chosenValues[0].toFixed(1);
            }
            output.text(outputStr);
        }
    })
}

function setupPopulationSlider() {
    let maxPopulation = $("#population-slider").attr("data-max-population");
    $("#population-slider").slider({
        min: 0,
        max: maxPopulation,
        step: maxPopulation / 1000,
        values: [0, maxPopulation],
        slide: function(event, ui) {
            let output = $("#population-output > span");
            let outputStr = ""
            let chosenValues = ui.values.sort((a,b) => {return (a - b)});
            if (chosenValues[0] < chosenValues[1]) {
                outputStr = numberFormatter(chosenValues[0], 1) + " - " + numberFormatter(chosenValues[1], 1);
            } else {
                outputStr = numberFormatter(chosenValues[0], 1);
            }
            output.text(outputStr);
        }
    })
}

function heatMapHandler(map) {
    $.ajax({
        url: "/api/city/rating",
        type: "GET",
        success: function(response){
            let heatMapData = [];
            response.forEach(function(city) {
                heatMapData.push([city.lat, city.lng, city.rating]);
            });
            let heat = L.heatLayer(heatMapData, {
                max: 10,
                radius: 50,
                blur: 15,
            })
            heat.addTo(map);
            map.removeLayer(heat);
            $(".city-tab").on("click", function() {
                if ($(this).attr("id") !== "heat-map-tab") {
                    map.removeLayer(heat);
                } else {
                    map.addLayer(heat);
                }
            })
        }
    });
}

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
                'query': $("#city-search-input").val(),
                'population': JSON.stringify($("#population-slider").slider("values").sort((a,b) => {return (a - b)})),
                'rating': JSON.stringify($("#rating-slider").slider("values").sort((a,b) => {return (a - b)})),
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
        $(".city-tab").on("click", function() {
            if ($(this).attr("id") !== currentTab) {
                map.removeLayer(marker.marker);
            } else {
                map.addLayer(marker.marker);
            }
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
