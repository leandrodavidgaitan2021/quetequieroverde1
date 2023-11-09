from flask import Blueprint, render_template, request, session, url_for, redirect, flash, g, jsonify, json
from datetime import datetime

# Importamos funcion para que que las vistas sea requerido logearse
from tienda.routers.auth import login_required, login_admin
from tienda.routers.articulos import crear


from tienda.modelos import articulo
from tienda.modelos import proveedor
from tienda.modelos import compra
from tienda.modelos import detalle_compra
from tienda.modelos import caja
from tienda import db


bp = Blueprint('compras', __name__, url_prefix='/compras')



# Lista los productos antes de logearse
@bp.route('/lista')
@login_required
def lista():
    #Almacena todos los proveedores en un lista para enviarlos 
    _proveedores = proveedor.Proveedor.query.all() 
    
    
    # Recibe un dato para buscar un articulo
    q = request.args.get('q')
    # Si recibio un dato para buscar lo filtra y lo guarda, 
    # SI NO manda la lista entera de articulos 
    if q:
        _articulos = articulo.Articulo.query.filter(
            articulo.Articulo.articulo.contains(q) | 
            articulo.Articulo.codart.contains(q) |
            articulo.Articulo.tipo.contains(q))
    else: 
        _articulos = articulo.Articulo.query.all()
#    print(_articulos)

    fecha = datetime.now().strftime("%Y-%m-%d")
    
    return render_template('compra/lista.html', articulos = _articulos, proveedores = _proveedores, fecha = fecha)


# Toda la compra se realiza en el cliente con JS y almacenando en localstorage


# Ruta para finalizar la compra recibida con AJAX
@bp.route('/finalizar_compra', methods=['POST'])
@login_required
def finalizar_compra():
    
    # Obtiene los datos enviados desde el cliente
    data = request.get_json()  
    fecha_data = data['fecha'] # Datos del lado del cliente, fecha seleccionado
    proveedor_data = data['proveedor']  # Datos del lado del cliente, proveedor seleccionado
    metodo_pago_data = data['metodo'] # Datos del lado del cliente, metodo de pago
    total_compra = data['totalcompra']  # Datos del lado del cliente, total compra
    carrito_data = data['carrito'] # Datos carrito de compras



#### Seccion para guardar la Compra ####    
    _fecha = datetime.strptime(fecha_data, "%Y-%m-%d").date()
    creado_por_ = g.user.id
    _proveedor_id = proveedor_data
    _metodo_pago = metodo_pago_data
    
    compra_ = compra.Compra(_fecha, _proveedor_id, _metodo_pago, creado_por_)
    cantidad_compra = compra.Compra.query.count()
    db.session.add(compra_)


# Seccion para actualizar caja        
    tipo_ = "C"
    
    if metodo_pago_data == "E":
        caja_ = metodo_pago_data
        monto_ = total_compra
        caja_ = caja.Caja(_fecha, tipo_, caja_, monto_, creado_por_)
        db.session.add(caja_)
    elif metodo_pago_data == "B":
        caja_ = metodo_pago_data
        monto_ = total_compra
        caja_ = caja.Caja(_fecha, tipo_, caja_, monto_, creado_por_)
        db.session.add(caja_)

    
#### Seccion para guardar la compra
    for articulo_carrito in carrito_data:
        _compra_id = cantidad_compra + 1
        _articulo_id =  articulo_carrito["id"]
        _cantidad = articulo_carrito["cantidad"]
        _costo_actualizado = articulo_carrito["costo"]
        _precio_unitario_actualizado = articulo_carrito["precio"]

        articulo_buscado= get_articulo(_articulo_id)


        if articulo_buscado:
            detalle_compra_ = detalle_compra.DetalleCompra(_compra_id, _articulo_id, _cantidad, _costo_actualizado)
            
            articulo_buscado.stock += _cantidad # actualiza stock de articulo Tabla ARTICULO
            articulo_buscado.costo = _costo_actualizado # actualiza costo de articulo Tabla ARTICULO
            articulo_buscado.precio = _precio_unitario_actualizado # actualiza precio de articulo Tabla ARTICULO
            db.session.add(detalle_compra_) # guarda TABLA DETALLE_COMPRA
            db.session.commit()


    # Devuelve una respuesta al cliente
    return jsonify({"mensaje": "Compra realizada con éxito"})





### metodo para buscar cliente por ID
def get_cliente(id):
    proveedor_buscado = proveedor.Proveedor.query.get_or_404(id)
    return proveedor_buscado

### metodo para buscar articulo por ID
def get_articulo(id):
    articulo_buscado = articulo.Articulo.query.get_or_404(id)
    return articulo_buscado