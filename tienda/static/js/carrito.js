let carritoTotal = 0;
document.addEventListener("DOMContentLoaded", function () {
    
    const listaArticulos = document.getElementById("lista-articulos");
    const carrito = document.getElementById("carrito");
    const total = document.getElementById("total");
    const agregarBotones = listaArticulos.querySelectorAll(".agregar");
    const cantidadInputs = listaArticulos.querySelectorAll(".cantidad");
    const stockInputs = listaArticulos.querySelectorAll(".stock");
    const precioInputs = listaArticulos.querySelectorAll(".precio");
    const vaciarCarritoBtn = document.getElementById("vaciar-carrito");
    const fechaSelect = document.getElementById("fecha");
    const clientesSelect = document.getElementById("clientes");
    const metodoPagoSelect = document.getElementById("metodo-pago");
    const finalizarVentaBtn = document.getElementById("finalizar-venta");

    agregarBotones.forEach((boton, index) => {
        boton.addEventListener("click", function () {
            var cantidadSelect = parseInt(cantidadInputs[index].value);
            var stock = parseInt(stockInputs[index].value);
            if (cantidadSelect <= stock) {
                const listItem = boton.parentNode;
                const articuloId = listItem.getAttribute("data-id");
                const articuloNombre = listItem.getAttribute("data-nombre");
                const articuloPrecio = parseInt(precioInputs[index].value);
                const cantidad = parseInt(cantidadInputs[index].value);
                
                let carritoItems = JSON.parse(localStorage.getItem("carrito")) || [];
                let articuloExistente = carritoItems.find(item => item.id === articuloId);

                if (articuloExistente) {
                    // Si el artículo ya está en el carrito, simplemente actualiza la cantidad
                    if (articuloExistente.cantidad+cantidad > stock){
                        alert("No hay suficuiente stock de este producto" );
                    } else {
                        articuloExistente.cantidad += cantidad;
                    }
                } else {
                    // Si no está en el carrito, agrégalo como un nuevo elemento
                    carritoItems.push({
                        id: articuloId,
                        nombre: articuloNombre,
                        precio: articuloPrecio,
                        cantidad: cantidad
                    });
                }

                
                // Actualiza el carrito en el almacenamiento local
                localStorage.setItem("carrito", JSON.stringify(carritoItems));

                // Actualiza la lista del carrito en la página
                actualizarCarrito(carritoItems);
            } else {
                alert("No hay suficuiente stock de este producto" );
            }
            
        });
    });

    // Función para actualizar la lista del carrito y calcular el total
    function actualizarCarrito(carritoItems) {
        carrito.innerHTML = "";
        
        carritoTotal = 0;
        if (carritoItems == 0){
            document.getElementById("finalizar-venta").disabled = true;
            document.getElementById("vaciar-carrito").disabled = true;
        } else {
            document.getElementById("finalizar-venta").disabled = false;
            document.getElementById("vaciar-carrito").disabled = false;
        }
        
        carritoItems.forEach(item => {
            const listItem = document.createElement("tr");

            const parrafo = document.createElement("td");
            parrafo.textContent = `${item.nombre} - $ ${item.precio} x ${item.cantidad} = $${(item.precio * item.cantidad).toFixed(2)}`;

            const botonBorrar = document.createElement("button");
            botonBorrar.classList.add("boton-borrar");
            botonBorrar.addEventListener("click", function () {
                borrarArticuloDelCarrito(item.id);
            });
            
            // Crea el icono y lo añade al botón
            const icono = document.createElement("i");
            icono.classList.add("bi", "bi-trash-fill");
            botonBorrar.appendChild(icono);
            
            listItem.appendChild(parrafo)
            listItem.appendChild(botonBorrar);
            carrito.appendChild(listItem);

            carritoTotal += item.precio * item.cantidad;
        });

        total.textContent = carritoTotal.toFixed(2);
    }


    // Función para mostrar la alerta con timeout y mensaje personalizado


    // Función para borrar un artículo del carrito
    function borrarArticuloDelCarrito(articuloId) {
        let carritoItems = JSON.parse(localStorage.getItem("carrito")) || [];
        carritoItems = carritoItems.filter(item => item.id !== articuloId);
        localStorage.setItem("carrito", JSON.stringify(carritoItems));
        actualizarCarrito(carritoItems);
    }

    // Vaciar completamente el carrito
    vaciarCarritoBtn.addEventListener("click", function () {

        Swal.fire({
            title: 'Vaciar Carrito?',
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
                localStorage.removeItem("carrito");
                carrito.innerHTML = "";
                total.textContent = "0.00";
                document.getElementById("finalizar-venta").disabled = true;
                document.getElementById("vaciar-carrito").disabled = true;
            }
          })
    });
            
    // Función para ocultar el mensaje flash después de un tiempo
    function ocultarMensaje() {
        var mensaje = document.getElementById('flash-message');
        setTimeout(function(){
            mensaje.style.display = 'none';
        }, 3000);  // Ocultar después de 3 segundos (puedes ajustar esto según tus necesidades)
    }

    // Carga el carrito almacenado en el LocalStorage al cargar la página
    const carritoAlmacenado = JSON.parse(localStorage.getItem("carrito")) || [];
    actualizarCarrito(carritoAlmacenado);

    // Finalizar la compra
    finalizarVentaBtn.addEventListener("click", function () {
        Swal.fire({
            title: 'Finalizar Venta?',
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
                const fechaSeleccionada = fechaSelect.value;
                const clienteSeleccionado = clientesSelect.value;
                const metodoPagoSeleccionado = metodoPagoSelect.value;
                const ventatotal = carritoTotal;
                const carritoItems = JSON.parse(localStorage.getItem("carrito")) || [];

                // Crear un objeto con el cliente y el carrito
                const compra = {
                    fecha: fechaSeleccionada,
                    cliente: clienteSeleccionado,
                    metodo: metodoPagoSeleccionado,
                    totalventa: ventatotal,
                    carrito: carritoItems
                
                };

                // Realizar una solicitud POST al servidor Flask
                fetch('/ventas/finalizar_venta', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(compra)
                })
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        alert("Error: " + data.error);
                    } else {
                        // Limpia el carrito y la página

                        localStorage.removeItem("carrito");
                        carrito.innerHTML = "";
                        total.textContent = "0.00";
                        ocultarMensaje();
                        location.reload();
                    }
                })
                .catch(error => {
                    alert("Error al realizar la venta: " + error);
                });
            }
        });
    });
});
