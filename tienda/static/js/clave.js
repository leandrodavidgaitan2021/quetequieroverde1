function enviarDatos() {
    var claveVieja = document.getElementById('claveVieja').value;
    var claveNueva1 = document.getElementById('claveNueva1').value;
    var claveNueva2 = document.getElementById('claveNueva2').value;

    if (claveNueva1 !== claveNueva2) {
        alert('Las nuevas contraseñas no coinciden.');
        return;
    }

    // Enviar datos a Flask
    fetch('/auth/cambiar_clave', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            claveVieja: claveVieja,
            claveNueva: claveNueva1,
        }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.mensaje);
        location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}