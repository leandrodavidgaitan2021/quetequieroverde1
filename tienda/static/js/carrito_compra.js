
let carritoTotal = 0;
document.addEventListener("DOMContentLoaded", function () {

    const listaArticulos = document.getElementById("lista-articulos");
    const carrito = document.getElementById("carrito");
    const total = document.getElementById("total");
    const agregarBotones = listaArticulos.querySelectorAll(".agregar");
    const cantidadInputs = listaArticulos.querySelectorAll(".cantidad");
    const costoInputs = listaArticulos.querySelectorAll(".costo");    
    const precioInputs = listaArticulos.querySelectorAll(".precio");
    const vaciarCarritoBtn = document.getElementById("vaciar-carrito");
    const fechaSelect = document.getElementById("fecha");
    const proveedoresSelect = document.getElementById("proveedores");
    const metodoPagoSelect = document.getElementById("metodo-pago");
    const finalizarCompraBtn = document.getElementById("finalizar-compra");

    agregarBotones.forEach((boton, index) => {
        boton.addEventListener("click", function () {
            const listItem = boton.parentNode;
            const articuloId = listItem.getAttribute("data-id");
            const articuloNombre = listItem.getAttribute("data-nombre");
            const articuloCosto = parseInt(costoInputs[index].value);            
            const articuloPrecio = parseInt(precioInputs[index].value);
            const cantidad = parseInt(cantidadInputs[index].value);
            
            
            let carritoItems = JSON.parse(localStorage.getItem("carrito-compra")) || [];
            let articuloExistente = carritoItems.find(item => item.id === articuloId);

            if (articuloExistente) {
                // Si el artículo ya está en el carrito, simplemente actualiza la cantidad
                articuloExistente.cantidad += cantidad;
            } else {
                // Si no está en el carrito, agrégalo como un nuevo elemento
                carritoItems.push({
                    id: articuloId,
                    nombre: articuloNombre,
                    costo: articuloCosto,
                    precio: articuloPrecio,
                    cantidad: cantidad
                });
            }

            // Actualiza el carrito en el almacenamiento local
            localStorage.setItem("carrito-compra", JSON.stringify(carritoItems));

            // Actualiza la lista del carrito en la página
            actualizarCarrito(carritoItems);
        });
    });

    // Función para actualizar la lista del carrito y calcular el total
    function actualizarCarrito(carritoItems) {
        carrito.innerHTML = "";

        carritoTotal = 0;
        carritoItems.forEach(item => {
            const listItem = document.createElement("li");
            listItem.classList.add("articulo-carrito");

            const parrafo = document.createElement("p")
            parrafo.classList.add("parrafo-articulo-carrito");
            parrafo.textContent = `${item.nombre} - $ ${item.costo} x ${item.cantidad} = $${(item.costo * item.cantidad).toFixed(2)}`;


            const botonBorrar = document.createElement("button");
            botonBorrar.classList.add("boton-borrar");
            botonBorrar.textContent = "Eliminar";
            botonBorrar.addEventListener("click", function () {
                borrarArticuloDelCarrito(item.id);
            });
            
            listItem.appendChild(parrafo)
            listItem.appendChild(botonBorrar);
            carrito.appendChild(listItem);

            carritoTotal += item.costo * item.cantidad;
            /*totalCarrito = carritoTotal*/
        });

        total.textContent = carritoTotal.toFixed(2);
    }

    // Función para borrar un artículo del carrito
    function borrarArticuloDelCarrito(articuloId) {
        let carritoItems = JSON.parse(localStorage.getItem("carrito-compra")) || [];
        carritoItems = carritoItems.filter(item => item.id !== articuloId);
        localStorage.setItem("carrito-compra", JSON.stringify(carritoItems));
        actualizarCarrito(carritoItems);
    }

    // Vaciar completamente el carrito
    vaciarCarritoBtn.addEventListener("click", function () {
        localStorage.removeItem("carrito-compra");
        carrito.innerHTML = "";
        total.textContent = "0.00";
    });

    // Carga el carrito almacenado en el LocalStorage al cargar la página
    const carritoAlmacenado = JSON.parse(localStorage.getItem("carrito-compra")) || [];
    actualizarCarrito(carritoAlmacenado);

    // Finalizar la compra
    finalizarCompraBtn.addEventListener("click", function () {
        const fechaSeleccionada = fechaSelect.value;
        console.log(fechaSeleccionada);
        const proveedorSeleccionado = proveedoresSelect.value;
        const metodoPagoSeleccionado = metodoPagoSelect.value;
        const totalCarrito = carritoTotal;
        console.log(totalCarrito)
        const carritoItems = JSON.parse(localStorage.getItem("carrito-compra")) || [];

        // Crear un objeto con el cliente y el carrito
        const compra = {
            fecha: fechaSeleccionada,
            proveedor: proveedorSeleccionado,
            metodo: metodoPagoSeleccionado,
            totalcompra: totalCarrito,
            carrito: carritoItems
        };

        // Realizar una solicitud POST al servidor Flask
        fetch('/compras/finalizar_compra', {
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
                alert("Compra finalizada con éxito.");
                                // La compra fue exitosa
                
                // Limpia el carrito y la página
                localStorage.removeItem("carrito-compra");
                carrito.innerHTML = "";
                total.textContent = "0.00";
                location.reload();
            }
        })
        .catch(error => {
            alert("Error al realizar la compra: " + error);
        });
    });
});