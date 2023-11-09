



document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = articulo.querySelector('.agregar-al-carro');

    addToCartButtons.forEach(articulo => {
      button.addEventListener('click', function() {
        const articuloId = this.getAttribute('dato-articulo-id');
        const articuloNombre= this.getAttribute('dato-articulo-nombre');
        const articuloPrecio = parseInt(articulo.querySelector('.precio').value);
        const carro = JSON.parse(localStorage.getItem('carro')) || [];
        
        // Busca si el artículo ya está en el carrito
        const existingItem = carro.find(item => item.articuloId === articuloId);

        if (existingItem) {
          existingItem.cantidad += 1;
        } else {
          carro.push({ articuloId, articuloNombre, articuloPrecio, cantidad: 1 });
        }

        localStorage.setItem('carro', JSON.stringify(carro));
      });
    });
  });

