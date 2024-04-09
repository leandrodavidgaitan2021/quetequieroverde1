from tienda import db


class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    fecha = db.Column(db.Date)
    cliente_id = db.Column(db.Integer)  
    
    def __init__(self, fecha, cliente_id, ):
        self.fecha = fecha
        self.cliente_id = cliente_id
