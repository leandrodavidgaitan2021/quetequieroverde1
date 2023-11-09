from tienda import db

# Modelo para la tabla de ventas
class Compra(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.Date)
    proveedor_id = db.Column(db.Integer)  
    metodo_pago = db.Column(db.String(1))
    creado_por = db.Column(db.Integer)
    
    def __init__(self, fecha, proveedor_id, metodo_pago, creado_por):
        self.fecha = fecha
        self.proveedor_id = proveedor_id
        self.metodo_pago = metodo_pago
        self.creado_por = creado_por
