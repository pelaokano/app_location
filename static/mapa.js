let validador = true;
let validador2 = true;
let polyline = null;
let marcador1 = null;
let marcador2 = null;
let puntoSeguir = null;
let socket = io.connect('http://192.168.0.164:8000');
let map = L.map('map').setView([41.3743, 2.1249], 15);

L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Tiles style by <a href="https://www.hotosm.org/" target="_blank">Humanitarian OpenStreetMap Team</a> hosted by <a href="https://openstreetmap.fr/" target="_blank">OpenStreetMap France</a>'
}).addTo(map);

socket.on('envio_datos', function (data) {
    console.log(data)
    document.getElementById("direccion").innerHTML = data["direccion"];
    document.getElementById("longitud").innerHTML = data["longitud"];
    document.getElementById("latitud").innerHTML = data["latitud"];

    map.setView([parseFloat(data["latitud"]), parseFloat(data["longitud"])], 30)
    let latlng1 = new L.latLng(data["latitud"], data["longitud"]);

    if (validador) {
        puntoSeguir = L.marker(latlng1).addTo(map);
        validador = false
    } else {
        map.removeLayer(puntoSeguir);
        puntoSeguir = L.marker(latlng1).addTo(map);
    }

})

socket.on('envio_temperatura', function (data) {
    console.log(data)
    document.getElementById("temperatura").innerHTML = data["temp_c"];
    document.getElementById("humedad").innerHTML = data["humid_pct"];
    document.getElementById("viento").innerHTML = data["windspd_kmh"];
})

socket.on('connect', function () {
    console.log('conectados!')
})

socket.on('disconnect', function () {
    console.log('desconectados!')
})
//lista de mapas para ir cambiando
//http://leaflet-extras.github.io/leaflet-providers/preview/

async function postData(url = '', dataPost) {
    const response = await fetch(url, {
        headers: { 'Content-Type': 'application/json' },
        method: 'POST',
        body: dataPost
    });
    return response.json();
};

function presBoton() {

    if (validador2) {

        data = postData("/ruta", JSON.stringify({ 'data': 'validador' }))
            .then(function (response) {
                if (response["data"] != 0) {

                    polyline = L.polyline(response["data"], { color: 'red' }).addTo(map);
                    map.fitBounds(polyline.getBounds());
                    marcador1 = L.marker(response["data"][0]).addTo(map);
                    marcador2 = L.marker(response["data"][response["data"].length - 1]).addTo(map);
                    validador2 = false;
                }
            });

    } else if (!validador2) {
        map.removeLayer(marcador1);
        map.removeLayer(marcador2);
        map.removeLayer(polyline);
        validador2 = true;
    }

};

if (window.performance) {
    console.info("Se actualiza la pagina");
    socket.emit('actualiza', {data: 'actualiza'});
  }
