from tienda import db

# Clase DetallePedido: 
class DetallePedido(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pedido_id = db.Column(db.Integer)
    articulo_id = db.Column(db.Integer)
    cantidad = db.Column(db.Integer, nullable = False)
    precio_unitario = db.Column(db.Integer, nullable = False)


    def __init__(self, pedido_id, articulo_id, cantidad, precio_unitario):
        self.pedido_id = pedido_id
        self.articulo_id = articulo_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
