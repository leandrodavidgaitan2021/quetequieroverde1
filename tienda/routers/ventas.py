from flask import Blueprint, render_template, request, url_for, redirect, flash, g, jsonify, json
from datetime import datetime

# Importamos funcion para que que las vistas sea requerido logearse
from tienda.routers.auth import login_required, login_admin



from tienda.modelos import articulo
from tienda.modelos import cliente
from tienda.modelos import venta
from tienda.modelos import detalle_venta
from tienda.modelos import caja
from tienda import db


bp = Blueprint('ventas', __name__, url_prefix='/ventas')



# Lista los productos antes de logearse
@bp.route('/lista')
@login_required
def lista():
    #Almacena todos los clientes en un lista para enviarlos 
    _clientes = cliente.Cliente.query.all() 
    
    
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
    return render_template('venta/lista.html', articulos = _articulos, clientes = _clientes, fecha = fecha)


# Toda la compra se realiza en el cliente con JS y almacenando en localstorage


# Ruta para finalizar la compra recibida con AJAX
@bp.route('/finalizar_venta', methods=['POST'])
@login_required
def finalizar_venta():
    data = request.get_json()  # Obtener los datos enviados desde el cliente
 
    fecha_data = data['fecha']    
    cliente_data = data['cliente']  # Datos cliente seleccionado
    metodo_pago_data = data['metodo'] # Datos metodo de pago
    total_venta = data['totalventa']  # Datos metodo de total
    carrito_data = data['carrito'] # Datos carrito de compras


#### Seccion para guardar la Venta ####    
#   fecha_actual = datetime.now() # toma la fecha actual
#    _fecha = fecha_actual
    _fecha = datetime.strptime(fecha_data, "%Y-%m-%d").date()

    _cliente_id = cliente_data
    creado_por_ = g.user.id

    venta_ = venta.Venta(_fecha, _cliente_id, metodo_pago_data, creado_por_)
    cantidad_venta = venta.Venta.query.count()
    db.session.add(venta_)


# Seccion para actualizar caja        
    tipo_ = "V"
    if metodo_pago_data == "E":
        caja_ = metodo_pago_data
        monto_ = total_venta
        caja_ = caja.Caja(_fecha, tipo_, caja_, monto_, creado_por_)
        db.session.add(caja_)
    elif metodo_pago_data == "B":
        caja_ = metodo_pago_data
        monto_ = total_venta
        caja_ = caja.Caja(_fecha, tipo_, caja_, monto_, creado_por_)
        db.session.add(caja_)



    
#### Seccion para guardar el carrito    
    for articulo_carrito in carrito_data:
        _venta_id = cantidad_venta + 1
        _articulo_id =  articulo_carrito["id"]
        _cantidad = articulo_carrito["cantidad"]
        _precio_unitario = articulo_carrito["precio"]

        articulo_buscado= get_articulo(_articulo_id)

        if articulo_buscado:
            if articulo_buscado.stock >= _cantidad:
                detalle_venta_ = detalle_venta.DetalleVenta(_venta_id, _articulo_id, _cantidad, _precio_unitario)
                articulo_buscado.stock -= _cantidad
                db.session.add(detalle_venta_)
                db.session.commit()
            else:
                return jsonify({"error": f"Stock insuficiente {articulo_buscado.articulo} para realizar la compra"}), 400

    # Devuelve una respuesta al cliente
    return jsonify({"mensaje": "Compra realizada con éxito"})





### metodo para buscar cliente por ID
def get_cliente(id):
    cliente_buscado = cliente.Cliente.query.get_or_404(id)
    return cliente_buscado

### metodo para buscar articulo por ID
def get_articulo(id):
    articulo_buscado = articulo.Articulo.query.get_or_404(id)
    return articulo_buscado