
document.getElementById('filtroInput').addEventListener('input', filtrarArticulos);



let productos = null; // Declara una variable para almacenar la lista de artículos

fetch('/pedidos/obtener_articulos')
    .then(response => {
        if (!response.ok) {
            throw new Error('Hubo un error al obtener los datos.');
            }
        return response.json();
    })
    .then(data => {
        // Asigna la lista de artículos obtenida a la variable
        console.log(productos);
        productos = data.arti;

        cargarProductos(productos);
    
  
        // Puedes trabajar con 'listaArticulos' aquí o utilizarlo en otras partes del código
        })
    .catch(error => {
        console.error('Error:', error);
        });

const contenedorProductos = document.querySelector("#contenedor-productos");
const botonesCategorias = document.querySelectorAll(".boton-categoria");
const tituloPrincipal = document.querySelector("#titulo-principal")
let botonesAgregar = document.querySelectorAll(".producto-agregar")
const numerito = document.querySelector("#numerito")
//console.log(productos); // Imprime la lista de artículos en la consola

function cargarProductos(productosElegidos) {

    contenedorProductos.innerHTML = "";
    console.log(productos);
      
    productosElegidos.forEach(producto => {
  
        const div = document.createElement("div");
        div.classList.add("producto");
        div.innerHTML =`
            <img class="producto-imagen" src="../static/${producto.imagen}" alt="${producto.titulo}">
            <div class="producto-detalles">
                <h3 class="producto-titulo">${producto.titulo}</h3>
                <p class="producto-precio">$ ${producto.precio}</p>
                <button class="producto-agregar" id="${producto.id}">Agregar</button>
            </div>
        `;
  
        contenedorProductos.append(div);
    })
    actualizarBotonesAgregar();
};

botonesCategorias.forEach(boton => {
    boton.addEventListener("click", (e) => {

        botonesCategorias.forEach(boton => boton.classList.remove("active"));
        e.currentTarget.classList.add("active");

        if (e.currentTarget.id != "todos") {
            const productoCategoria = productos.find(producto => producto.categoria.id === e.currentTarget.id);
            tituloPrincipal.innerHTML = productoCategoria.categoria.nombre;
            
            const productosBoton = productos.filter(producto => producto.categoria.id === e.currentTarget.id);
            cargarProductos(productosBoton);
        } else {
            tituloPrincipal.innerHTML = "Todos los productos"
            cargarProductos(productos);
        }

    })
});

function actualizarBotonesAgregar(){
    botonesAgregar = document.querySelectorAll(".producto-agregar")

    botonesAgregar.forEach(boton => {
        boton.addEventListener("click", agregarAlCarrito);
    })
};


let productosEnCarrito;
    
let productosEnCarritoLS = localStorage.getItem("productos-en-carrito");
  
if (productosEnCarritoLS) {
    productosEnCarrito = JSON.parse(productosEnCarritoLS);
    actualizarNumerito();
} else {
    productosEnCarrito = [];
};
  
console.log(productos);

function agregarAlCarrito(e) {
    const idBoton = e.currentTarget.id;
    const productoAgregado = productos.find(producto => producto.id === idBoton);

    if (productosEnCarrito.some(producto => producto.id === idBoton)) {
        const index = productosEnCarrito.findIndex(producto => producto.id === idBoton);
        productosEnCarrito[index].cantidad++;
    } else {
        productoAgregado.cantidad = 1;
        productosEnCarrito.push(productoAgregado);
    }
    actualizarNumerito();

    localStorage.setItem("productos-en-carrito", JSON.stringify(productosEnCarrito));

};

function actualizarNumerito() {
    let nuevoNumerito = productosEnCarrito.reduce((acc, producto) => acc + producto.cantidad, 0)
    numerito.innerHTML = nuevoNumerito;
}

function confirmLogout() {
    if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
        window.location.href = '/auth/logout';
    } else {
        // Si el usuario cancela, vuelve a la página de inicio
        window.location.href = '';
    }
}



function filtrarArticulos() {
    const input = document.getElementById('filtroInput');
    const filtro = input.value.toUpperCase();
  
    const listaFiltrada = productos.filter(item => {
      return item.titulo.toUpperCase().indexOf(filtro) > -1;
    });
    console.log('lista filtrada', listaFiltrada);
    cargarProductos(listaFiltrada);
  }