from tienda import db

# Clase DetalleVenta: 
class DetalleVenta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    venta_id = db.Column(db.Integer)
    articulo_id = db.Column(db.Integer)
    cantidad = db.Column(db.Integer, nullable = False)
    precio_unitario = db.Column(db.Integer, nullable = False)


    def __init__(self, venta_id, articulo_id, cantidad, precio_unitario):
        self.venta_id = venta_id
        self.articulo_id = articulo_id
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
