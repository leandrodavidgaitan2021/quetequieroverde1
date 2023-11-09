from tienda import db

# Modelo para la tabla de ventas
class Venta(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.Date)
    cliente_id = db.Column(db.Integer)  # Puedes agregar una relación con la tabla de clientes si es necesario
    metodo_pago = db.Column(db.String(1))
    creado_por = db.Column(db.Integer)
    
    def __init__(self, fecha, cliente_id, metodo_pago, creado_por):
        self.fecha = fecha
        self.cliente_id = cliente_id
        self.metodo_pago = metodo_pago
        self.creado_por = creado_por
