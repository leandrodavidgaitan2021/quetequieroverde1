from tienda.modelos import articulo, proveedor, categoria, cliente, caja, venta, compra, detalle_compra, detalle_venta, user

#from tienda.modelos import pedido, detalle_pedido, cuenta_corriente, transaccion

from datetime import datetime


# ********************* Busquedas de ARTICULOS

def buscar_articulos(q):
    return articulo.Articulo.query.filter(
            articulo.Articulo.articulo.contains(q) | 
            articulo.Articulo.codart.contains(q) |
            articulo.Articulo.proveedor.contains(q) |
            articulo.Articulo.tipo.contains(q))


def buscar_id_articulo(id):
    return articulo.Articulo.query.get_or_404(id)


def buscar_cod_articulo(_codart):
    return articulo.Articulo.query.filter_by(codart = _codart).first()


def buscar_tipo_articulo(_tipo):
    return articulo.Articulo.query.filter_by(tipo = _tipo).all()


def buscar_proveedor_articulo(_proveedor):
    return articulo.Articulo.query.filter_by(proveedor = _proveedor).all()

def buscar_todos_articulos():
    return articulo.Articulo.query.all()

def buscar_todos_provee_tipo_articulos(_proveedor, _tipo):
    return articulo.Articulo.query.filter_by(proveedor = _proveedor).filter_by(tipo = _tipo).all()    



# ********************* Busquedas de PROVEEDORES
def buscar_todos_proveedores():
    return proveedor.Proveedor.query.all()

def buscar_q_proveedores(q):
    return proveedor.Proveedor.query.filter(proveedor.Proveedor.razonsocial.contains(q))

def buscar_razon_proveedores(_razonsocial):
    return proveedor.Proveedor.query.filter_by(razonsocial = _razonsocial).first()

def buscar_cuit_proveedores(_cuit):
    return proveedor.Proveedor.query.filter_by(cuit = _cuit).first()

def buscar_id_proveedor(id):
    return proveedor.Proveedor.query.get_or_404(id)
     
    



# ********************* Busqueda de CATEGORIAS    
def buscar_todas_categorias():   
    return categoria.Categoria.query.all()

def buscar_q_categorias(q):
    return categoria.Categoria.query.filter(categoria.Categoria.categoria.contains(q))

def buscar_categoria(_categoria):
    return categoria.Categoria.query.filter_by(categoria = _categoria).first()

def buscar_id_categoria(id):
    return categoria.Categoria.query.get_or_404(id)



# ********************* Busquedas de CLIENTES
def buscar_todos_clientes():
    return cliente.Cliente.query.all()

def buscar_q_clientes(q):
    return cliente.Cliente.query.filter(cliente.Cliente.nombre.contains(q))

def buscar_nombre_clientes(_nombre):
    return cliente.Cliente.query.filter_by(nombre = _nombre).first()

def buscar_id_clientes(id):
    return cliente.Cliente.query.get_or_404(id)

def buscar_cuit_usuarios(_cuit):
    return cliente.Cliente.query.filter_by(cuit = _cuit).first()

def buscar_mail_clientes(_mail):
    return cliente.Cliente.query.filter_by(email = _mail).first()


# ********************* Busquedas de USER
def buscar_id_usuario(id):
    return user.User.query.get_or_404(id)

def buscar_mail_users(_mail):
    return user.User.query.filter_by(email = _mail).first()




# ********************* FECHAS
def fecha_hora_actual():
    return datetime.now().strftime("%Y-%m-%d")

def fecha_actual():
    return datetime.now()

def guarda_fecha(fecha_data):
    return datetime.strptime(fecha_data, "%Y-%m-%d").date()

def fecha_a_mostrar(fecha):
    # Formatear la fecha actual en modo latino
    mostrar = fecha.strftime('%d/%m/%Y')
    print(mostrar)
    return mostrar



# ********************* COMPRAS
def buscar_compra(identifica):
    return compra.Compra.query.filter_by(id = identifica).first()


# ********************* DETALLE COMPRAS
def buscar_detalle_compra(compraid_id):
    return detalle_compra.DetalleCompra.query.filter_by(compra_id = compraid_id).all()




# ********************* VENTAS
def buscar_venta(identifica):
    return venta.Venta.query.filter_by(id = identifica).first()



# ********************* DETALLE VENTAS
def buscar_detalle_venta(ventaid_id):
    return detalle_venta.DetalleVenta.query.filter_by(venta_id = ventaid_id).all()




# ********************* CAJAS

def buscar_operacion(identificador):
    return caja.Caja.query.get_or_404(identificador)
     

"""
# ********************* CUENTA CORRIENTE

def buscar_cuenta(identificador):
    return cuenta_corriente.CuentaCorriente.query.filter_by(cliente_id = identificador).first()

def buscar_todas_cuentas():
    return cuenta_corriente.CuentaCorriente.query.all()


# ********************* TRANSACCIONES
def buscar_transacciones_cliente(identificador):
    return transaccion.Transaccion.query.filter_by(cliente_id = identificador).all()

def buscar_todas_transaciones():
    return transaccion.Transaccion.query.all()


# *********************** PEDIDOS
def buscar_todos_pedidos():
    return pedido.Pedido.query.all()

def buscar_todos_pedidos_desc():
    # se guardan todas las cajas por id usuario = creado_por
    return pedido.Pedido.query.order_by(pedido.Pedido.id.desc()).all()

def buscar_pedido(identifica):
    return pedido.Pedido.query.filter_by(id = identifica).first()


# ********************* DETALLE PEDIDO
def buscar_detalle_pedido(pedidoid_id):
    return detalle_pedido.DetallePedido.query.filter_by(pedido_id = pedidoid_id).all()



# ***************** GET PEDIDO
def get_pedido(identifica):

    detalles = []
    
    pedidoid = buscar_pedido(identifica)
    
    detalle_pedido_buscada = buscar_detalle_pedido(pedidoid.id)
    
    _cliente = buscar_id_usuarios(pedidoid.cliente_id)
    
    _vendedor = buscar_id_usuarios(_cliente.idvendedor)
    
    vendedor = {
            'id' : str(_vendedor.id),
            'username' : _vendedor.username,
            'tdescuento' : _vendedor.tdescuento,
        }


    total = 0
    for detalle_ped in detalle_pedido_buscada:
        
        articulo_buscado = buscar_cod_articulo(detalle_ped.articulo_codart)

        if articulo_buscado:
            precioConDescuento = detalle_ped.precio_unitario
            if _vendedor.tdescuento > 0:
                porcentaje = _vendedor.tdescuento
                precioOriginal = detalle_ped.precio_unitario
                descuento = (porcentaje / 100) * precioOriginal
                precioConDescuento = precioOriginal - descuento

            detalle = {
                'id' : str(articulo_buscado.id),
                'articulo' : articulo_buscado.articulo,
                'precio' : detalle_ped.precio_unitario,
                'precio_descuento' : precioConDescuento,
                'cantidad' : detalle_ped.cantidad
            }
            
            detalles.append(detalle)
            total = total + (detalle_ped.cantidad * detalle_ped.precio_unitario)
            
    print(detalles)

    return total, detalles, vendedor

"""



# ******************GET VENTA
def get_venta(identifica):

    detalles = []

    ventaid = buscar_venta(identifica)

    cliente_buscado = buscar_id_clientes(ventaid.cliente_id)    
    
    detalle_venta_buscada = buscar_detalle_venta(ventaid.id)
    
    for detalle_art in detalle_venta_buscada:

        articulo_buscado = buscar_id_articulo(detalle_art.articulo_id)

        if articulo_buscado:
            detalle = {
                'id' : str(articulo_buscado.id),
                'articulo' : articulo_buscado.articulo,
                'cantidad' : detalle_art.cantidad,
                'precio' : detalle_art.precio_unitario,
                'cantidad' : detalle_art.cantidad
            }
            detalles.append(detalle)

    return cliente_buscado, detalles

# GET COMPRA
def get_compra(identifica):
    detalles = []
    
    compraid = buscar_compra(identifica)

    proveedor_buscado = buscar_id_proveedor(compraid.proveedor_id)
    
    detalle_compra_buscada = buscar_detalle_compra(compraid.id)

    for detalle_art in detalle_compra_buscada:
        
        articulo_buscado = buscar_id_articulo(detalle_art.articulo_id)
        
        if articulo_buscado:
            detalle ={
                'articulo' : articulo_buscado.articulo,
                'cantidad' : detalle_art.cantidad,
                'precio' : detalle_art.precio_unitario
            }
            detalles.append(detalle)
            
    return proveedor_buscado, detalles

