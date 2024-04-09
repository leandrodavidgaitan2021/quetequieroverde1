  function mostrarVistaPrevia() {
    const archivoInput = document.getElementById('archivoInput');
    const vistaPrevia = document.getElementById('vistaPrevia');
    const imagenPrevia = document.getElementById('imagenPrevia');
  
    if (archivoInput.files.length > 0) {
      const archivo = archivoInput.files[0];
      const lector = new FileReader();
  
      lector.onload = function(e) {
        imagenPrevia.src = e.target.result;
        vistaPrevia.style.display = 'block';
      };
  
      lector.readAsDataURL(archivo);
    }
  }