
function eliminarPDF() {
    var nombrePDF = document.getElementById('pdf').value; // Nombre del archivo PDF
    fetch('/cajas/eliminar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({nombre_pdf: nombrePDF})
    }).then(response => {
        if (response.ok) {
            alert("PDF eliminardo correctamente");
        } else {
            alert("Error al eliminar el PDF");
        }
    }).catch(error => {
        console.error('Error al eliminar pdf la solicitud:', error);
    });
    window.history.go(-1)
}