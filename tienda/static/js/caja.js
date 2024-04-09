function enviarDatos() {
    var fecha = document.getElementById('fecha').value;
    var opcion = document.getElementById('opcion').value;
    var monto = document.getElementById('monto').value;

    // Enviar datos a Flask
    fetch('/cajas/transferencia', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            fecha: fecha,
            opcion: opcion,
            monto: monto
        }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.mensaje);
        window.history.go(-1);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.getElementById("aceptar").addEventListener("click", function() {
    Swal.fire({
        title: 'Finalizar Transferencia?',
        text: "No podrás revertir esto!",
        icon: 'warning',
        width: '300px',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Si',
        cancelButtonText: 'No'
        }).then((result) => {
        if (result.isConfirmed) {
            enviarDatos();
        }
    });
});

// Función para enviar los datos a Flask con AJAX
/*function enviarDatos(fecha, opcion, monto) {
    
    var xhr = new XMLHttpRequest();
    var url = './transferir'; // La URL de la vista de Flask que manejará los datos
    var data = {
       fecha: fecha,
        opcion: opcion,
        monto: monto
    };
    xhr.open('POST', url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4 && xhr.status == 200) {
            // Aquí puedes manejar la respuesta de Flask si es necesario
            resultados.innerHTML = "Datos enviados a Flask con éxito.";
            location.reload();
            }
        };
        xhr.send(JSON.stringify(data));
    }
});
*/