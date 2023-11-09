let productosEnCarrito = localStorage.getItem("carro");
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
                <div class="carrito-producto-titulo">
                    <small>Articulo</small>
                    <h5>${producto.articuloNombre}</h5>
                </div>
                <div class="carrito-producto-cantidad">
                    <small>Cantidad</small>
                    <p>${producto.cantidad}</p>
                </div>
                <div class="carrito-producto-precio">
                    <small>Precio</small>
                    <p>${producto.articuloPrecio}</p>                            
                </div>
                <div class="carrito-producto-subtotal">
                    <small>Subtotal</small>
                    <p>$ ${producto.articuloPrecio * producto.cantidad}</p>                            
                </div>
                <button class="carrito-producto-eliminar" id="${producto.articuloId}"><i class="bi bi-trash-fill"></i></button>
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


    const index = productosEnCarrito.findIndex(producto => producto.articuloId === idBoton);
    productosEnCarrito.splice(index, 1);
    cargarProductosCarrito();

    localStorage.setItem("carro", JSON.stringify(productosEnCarrito));

}

botonVaciar.addEventListener("click", vaciarCarrito);
function vaciarCarrito() {
    productosEnCarrito.length = 0;
    localStorage.setItem("carro", JSON.stringify(productosEnCarrito));
    cargarProductosCarrito();

}


function actualizarTotal() {
    const totalCalculado = productosEnCarrito.reduce((acc, producto) => acc + (producto.articuloPrecio * producto.cantidad), 0);
    total.innerHTML = `$ ${totalCalculado}`;
}


botonComprar.addEventListener("click", comprarCarrito);
function comprarCarrito() {
    productosEnCarrito.length = 0;
    localStorage.setItem("carro", JSON.stringify(productosEnCarrito));
    
    contenedorCarritoVacio.classList.add("disable");
    contenedorCarritoProductos.classList.add("disable");
    contenedorCarritoAcciones.classList.add("disable"); 
    contenedorCarritoComprado.classList.remove("disable"); 

}