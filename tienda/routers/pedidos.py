from flask import Blueprint, render_template, request, url_for, redirect, flash, g, jsonify, json


# Importamos funcion para que que las vistas sea requerido logearse
from tienda.routers.auth import login_required, login_admin
from tienda.routers.busquedas import * 


from tienda.modelos import articulo
from tienda.modelos import cliente

from tienda.modelos import pedido
from tienda.modelos import detalle_pedido
from tienda import db


bp = Blueprint('pedidos', __name__, url_prefix='/pedidos')



# Lista los productos antes de logearse
@bp.route('/principal')
@login_required
def principal():
    fecha = fecha_hora_actual()
    return render_template('pedido/principal.html', fecha = fecha)




@bp.route('/obtener_articulos')
@login_required
def obtener_articulos():
    _articulos = buscar_todos_articulos()
    # Serializa los objetos de usuario a un formato JSON
    articulos_json = [articulo.serialize() for articulo in _articulos]
#    print(articulos_json)
    return jsonify(arti=articulos_json)
    
# Lista los productos antes de logearse
@bp.route('/carrito')
@login_required
def carrito():
    return render_template('pedido/carrito.html')


"""
    def serialize(self):
        return {
            'id': self.codart,
            'titulo': self.articulo,
            'imagen': self.imgfile,
            'categoria': {
                'nombre': self.tipo,
                'id': self.tipo.lower()
            },
            'precio': self.precio
        }


class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.Date)
    cliente_id = db.Column(db.Integer)  
    
    def __init__(self, fecha, cliente_id, ):
        self.fecha = fecha
        self.cliente_id = cliente_id
        
class DetallePedido(db.Model):        
    id = db.Column(db.Integer, primary_key = True)
    pedido_id = db.Column(db.Integer)
    articulo_id = db.Column(db.Integer)
    cantidad = db.Column(db.Integer, nullable = False)
    precio_unitario = db.Column(db.Integer, nullable = False)

"""




# Ruta para finalizar la compra recibida con AJAX
@bp.route('/finalizar_pedido', methods=['POST'])
@login_required
def finalizar_pedido():
    data = request.get_json()  # Obtener los datos enviados desde el cliente

    carrito_data = data['carrito'] # Datos carrito de compras

    _fecha = fecha_hora_actual()

    _fecha = guarda_fecha(_fecha)

    _cliente_id = g.user.id


    pedido_ = pedido.Pedido(_fecha, _cliente_id)
    cantidad_pedido = pedido.Pedido.query.count()
    db.session.add(pedido_)
    
    _pedido_id = cantidad_pedido + 1

#### Seccion para guardar el carrito    
    for articulo_carrito in carrito_data:

        _articulo_codart =  articulo_carrito["id"]
        _cantidad = articulo_carrito["cantidad"]
        _precio_unitario = articulo_carrito["precio"]

        detalle_venta_ = detalle_pedido.DetallePedido(_pedido_id, _articulo_codart, _cantidad, _precio_unitario)
        db.session.add(detalle_venta_)
        db.session.commit()
        flash("Venta realizada con éxito")
    
    
    # Devuelve una respuesta al cliente
    return jsonify({"mensaje": "Pedido realizada con éxito"})





