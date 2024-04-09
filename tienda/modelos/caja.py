from tienda import db

# Modelo para la tabla de ventas
class Caja(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.Date)
    tipo = db.Column(db.String(1))  #Tipo: VENTA, COMPRA, TRANSFERENCIA 
    id_tipo = db.Column(db.Integer) #id venta o compra
    caja = db.Column(db.String(1))  # Caja: EFECTIVO, BILLETERA
    monto = db.Column(db.Integer)
    creado_por = db.Column(db.Integer, nullable = False) 
    
    def __init__(self, fecha, tipo, id_tipo, caja, monto, creador_por):
        self.fecha = fecha
        self.tipo = tipo
        self.id_tipo = id_tipo
        self.caja = caja
        self.monto = monto
        self.creado_por = creador_por
