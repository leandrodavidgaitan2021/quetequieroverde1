from flask import Blueprint, render_template, request, url_for, redirect, flash, g, jsonify, json


# Importamos funcion para que que las vistas sea requerido logearse
from tienda.routers.auth import login_required, login_admin
from tienda.routers.busquedas import * 



from tienda.modelos import venta
from tienda.modelos import detalle_venta
from tienda.modelos import caja
from tienda import db


bp = Blueprint('ventas', __name__, url_prefix='/ventas')



# Lista los productos antes de logearse
@bp.route('/lista')
@login_required
@login_admin
def lista():
    #Almacena todos los clientes en un lista para enviarlos 

    _clientes = buscar_todos_clientes()
    
    # Recibe un dato para buscar un articulo
    q = request.args.get('q')
    # Si recibio un dato para buscar lo filtra y lo guarda, 
    # SI NO manda la lista entera de articulos 
    if q:
        _articulos = buscar_articulos(q)
    else: 
        _articulos = buscar_todos_articulos()

    fecha = fecha_hora_actual()
    
    return render_template('venta/lista.html', articulos = _articulos, clientes = _clientes, fecha = fecha)


# Toda la compra se realiza en el cliente con JS y almacenando en localstorage


# Ruta para finalizar la compra recibida con AJAX
@bp.route('/finalizar_venta', methods=['POST'])
@login_required
@login_admin
def finalizar_venta():
    data = request.get_json()  # Obtener los datos enviados desde el cliente
 
    fecha_data = data['fecha']    
    cliente_data = data['cliente']  # Datos cliente seleccionado
    metodo_pago_data = data['metodo'] # Datos metodo de pago
    total_venta = data['totalventa']  # Datos metodo de total
    carrito_data = data['carrito'] # Datos carrito de compras


#### Seccion para guardar la Venta ####    
    _fecha = guarda_fecha(fecha_data)

    _cliente_id = cliente_data
    creado_por_ = g.user.id

    venta_ = venta.Venta(_fecha, _cliente_id, metodo_pago_data, creado_por_)
    cantidad_venta = venta.Venta.query.count()
    db.session.add(venta_)


# Seccion para actualizar caja        
    tipo_ = "V"
    id_tipo_ = cantidad_venta + 1
    caja_ = metodo_pago_data
    monto_ = total_venta    
    caja_ = caja.Caja(_fecha, tipo_, id_tipo_, caja_, monto_, creado_por_)
    db.session.add(caja_)

    _venta_id = cantidad_venta + 1

    guardar = True
#### Seccion para guardar el carrito    
    for articulo_carrito in carrito_data:

        _articulo_id =  articulo_carrito["id"]
        _cantidad = articulo_carrito["cantidad"]
        _precio_unitario = articulo_carrito["precio"]

        articulo_buscado= buscar_id_articulo(_articulo_id)

        if articulo_buscado:
            if articulo_buscado.stock >= _cantidad:
                detalle_venta_ = detalle_venta.DetalleVenta(_venta_id, _articulo_id, _cantidad, _precio_unitario)
                articulo_buscado.stock -= _cantidad
                db.session.add(detalle_venta_)
            else:
                guardar = False

   
    if guardar:
        db.session.commit()
        flash("Venta realizada con éxito")
    else:
        db.session.rollback()
        return jsonify({"error": "Stock insuficiente para realizar la compra"}), 400
    
    
    # Devuelve una respuesta al cliente
    return jsonify({"mensaje": "Compra realizada con éxito"})



