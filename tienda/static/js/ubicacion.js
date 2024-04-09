function obtenerUbicacion() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var latitud = position.coords.latitude;
            var longitud = position.coords.longitude;

            document.getElementById("ubicacion").innerHTML = "Ubicación: " + latitud + ", " + longitud;

            obtenerInformacionUbicacion(latitud, longitud);
        }, function(error) {
            console.error("Error al obtener la ubicación: ", error.message);
        });
    } else {
        alert("La geolocalización no es compatible con este navegador.");
    }
}

function obtenerInformacionUbicacion(latitud, longitud) {
    var apiUrl = `https://nominatim.openstreetmap.org/reverse?lat=${latitud}&lon=${longitud}&format=json`;

    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            // Extraer el código postal, localidad, provincia, pais de la respuesta
            var codigoPostal = data.address.postcode;
            var localidad = data.address.city || data.address.town || data.address.village;
            var provincia = data.address.state;
            var pais = data.address.country;
            
            // Mostrar el código postal, localidad, provincia, pais en el elemento con id "codigo-postal", "localidad", "provincia", "pais"
            document.getElementById("codigo-postal").innerHTML = "Código Postal: " + codigoPostal;
            document.getElementById("localidad").innerHTML = "Localidad: " + localidad;
            document.getElementById("provincia").innerHTML = "Provincia: " + provincia;
            document.getElementById("pais").innerHTML = "País: " + pais;
        })
        .catch(error => {
            console.error("Error al obtener la información de ubicación: ", error);
        });
}