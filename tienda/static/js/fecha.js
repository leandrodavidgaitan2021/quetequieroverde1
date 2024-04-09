var fechasElementos = document.querySelectorAll('.fecha'); // Obtener todos los elementos con la clase 'fecha'
fechasElementos.forEach(function(elemento) {
    var fechaISO = elemento.innerText.trim(); // Obtener el texto de la fecha
    var partes = fechaISO.split('-'); // Dividir la cadena en partes (año, mes, día)
    var nuevaFecha = partes[2] + '-' + partes[1] + '-' + partes[0]; // Reordenar las partes en el nuevo formato 'dd-mm-aaaa'
    elemento.innerText = nuevaFecha; // Actualizar el contenido del elemento con la nueva fecha

});

