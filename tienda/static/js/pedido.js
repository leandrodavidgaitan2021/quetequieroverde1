let productosEnCarrito = localStorage.getItem("productos-en-carrito");
productosEnCarrito = JSON.parse(productosEnCarrito);

const contenedorCarritoVacio = document.querySelector("#carrito-vacio");
const contenedorCarritoProductos = document.querySelector("#carrito-productos");
const contenedorCarritoAcciones = document.querySelector("#carrito-acciones");
const contenedorCarritoComprado = document.querySelector("#carrito-comprado");
let botonesEliminar = document.querySelectorAll(".carrito-botones-eliminar");
const botonVaciar = document.querySelector("#carrito-acciones-vaciar");
const botonComprar = document.querySelector("#carrito-acciones-comprar");
const contenedorTotal = document.querySelector("#total");



function cargarProductosCarrito() {
    if (productosEnCarrito && productosEnCarrito.length > 0) {
        

        contenedorCarritoVacio.classList.add("disable");
        contenedorCarritoProductos.classList.remove("disable");
        contenedorCarritoAcciones.classList.remove("disable"); 
        contenedorCarritoComprado.classList.add("disable"); 
        
        contenedorCarritoProductos.innerHTML = "";
        
        productosEnCarrito.forEach(producto =>{
            const div = document.createElement("div");
            div.classList.add("carrito-producto");
            div.innerHTML = `
                <img class="carrito-producto-imagen" src="../static/${producto.imagen}" alt="${producto.titulo}">
                <div class="carrito-producto-titulo">
                    <small>Titulo</small>
                    <h3>${producto.titulo}</h3>
                </div>
                <div class="carrito-producto-cantidad">
                    <small>Cantidad</small>
                    <p>${producto.cantidad}</p>
                </div>
                <div class="carrito-producto-precio">
                    <small>Precio</small>
                    <p>${producto.precio}</p>                            
                </div>
                <div class="carrito-producto-subtotal">
                    <small>Subtotal</small>
                    <p>$ ${producto.precio * producto.cantidad}</p>                            
                </div>
                <button class="carrito-producto-eliminar" id="${producto.id}"><i class="bi bi-trash-fill"></i></button>
            ` 
            contenedorCarritoProductos.append(div);

        })
    } else {
        contenedorCarritoVacio.classList.remove("disable");
        contenedorCarritoProductos.classList.add("disable");
        contenedorCarritoAcciones.classList.add("disable"); 
        contenedorCarritoComprado.classList.add("disable"); 
    };
    actualizarBotonesEliminar();
    actualizarTotal();
};

cargarProductosCarrito();




function actualizarBotonesEliminar(){
    botonesEliminar = document.querySelectorAll(".carrito-producto-eliminar")

    botonesEliminar.forEach(boton => {
        boton.addEventListener("click", eliminarDelCarrito);
    })
};

function eliminarDelCarrito(e) {
    const idBoton = e.currentTarget.id;


    const index = productosEnCarrito.findIndex(producto => producto.id === idBoton);
    productosEnCarrito.splice(index, 1);
    cargarProductosCarrito();

    localStorage.setItem("productos-en-carrito", JSON.stringify(productosEnCarrito));

}

botonVaciar.addEventListener("click", vaciarCarrito);
function vaciarCarrito() {
    productosEnCarrito.length = 0;
    localStorage.setItem("productos-en-carrito", JSON.stringify(productosEnCarrito));
    cargarProductosCarrito();

}


function actualizarTotal() {
    const totalCalculado = productosEnCarrito.reduce((acc, producto) => acc + (producto.precio * producto.cantidad), 0);
    total.innerHTML = `$ ${totalCalculado}`;
}


botonComprar.addEventListener("click", comprarCarrito);
function comprarCarrito() {
    Swal.fire({
        title: 'Finalizar Pedido?',
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
            //const fechaSeleccionada = fechaSelect.value;
            //const clienteSeleccionado = clientesSelect.value;
            //const metodoPagoSeleccionado = metodoPagoSelect.value;
            //const ventatotal = totalCalculado;
            const carritoItems = JSON.parse(localStorage.getItem("productos-en-carrito")) || [];

            // Crear un objeto con el cliente y el carrito
            const compra = {
                //fecha: fechaSeleccionada,
                //cliente: clienteSeleccionado,
                //metodo: metodoPagoSeleccionado,
                //totalventa: ventatotal,
                carrito: carritoItems
            
            };

            // Realizar una solicitud POST al servidor Flask
            fetch('/pedidos/finalizar_pedido', {
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

                    localStorage.removeItem("productos-en-carrito");
                    //carrito.innerHTML = "";
                    //total.textContent = "0.00";
                    productosEnCarrito.length = 0;
                    //localStorage.setItem("productos-en-carrito", JSON.stringify(productosEnCarrito));
                    
                    contenedorCarritoVacio.classList.add("disable");
                    contenedorCarritoProductos.classList.add("disable");
                    contenedorCarritoAcciones.classList.add("disable"); 
                    contenedorCarritoComprado.classList.remove("disable"); 
                    //ocultarMensaje();
                    location.reload();
                }
            })
            .catch(error => {
                alert("Error al realizar la pedido: " + error);
            });
        }
    });
    


}