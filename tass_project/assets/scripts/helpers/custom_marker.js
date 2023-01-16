export default class CustomMarker {
    constructor(lat, lng, label, color, rating) {
        this.rating = parseFloat(rating).toFixed(1);
        this.uuid = "S" + Math.random().toString(16).slice(2);
        this.marker = new L.Marker([lat, lng], {
            icon: this.setupStyle(color)
        });
        this.marker.bindPopup(label);
    }

    changeColor(color) {
        $('#' + this.uuid).find('span').css('background-color', color);
    }

    getRandomColor() {
        return '#'+(Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0');
    }

    setupStyle(color) {
        const markerHtmlStyles = `
            background-color: ${color};
            width: 2rem;
            height: 2rem;
            display: block;
            left: -1rem;
            top: -1rem;
            position: relative;
            border-radius: 3rem 3rem 0;
            transform: rotate(45deg);
            border: 1px solid #FFFFFF`
        const textStyle = `
            position: relative;
            left: -0.55rem;
            top: -2.5rem;
            text-align: center;
        `
        return L.divIcon({
            className: "custom-pin",
            iconAnchor: [0, 24],
            labelAnchor: [-6, 0],
            popupAnchor: [0, -36],
            html: `<div id="${this.uuid}"><span style="${markerHtmlStyles}"></span><p style="${textStyle}">${this.rating}</p></div>`
        })
    }
}