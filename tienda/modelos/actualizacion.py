from tienda import db

# Clase Actualizacion: 
class Actualizacion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    proveedor = db.Column(db.String(50), nullable = False)
    tipo = db.Column(db.String(20), nullable = False)
    costo = db.Column(db.Integer, nullable = False)
    ganancia = db.Column(db.Integer, nullable = False)
    creado_por = db.Column(db.Integer, nullable = False) 
    
    
    def __init__(self, proveedor, tipo, costo, ganancia, creado_por):
        self.proveedor = proveedor   
        self.tipo = tipo
        self.costo = costo
        self.ganancia = ganancia
        self.creado_por = creado_por

        
    def __repr__(self):
        return f'<Costo: {self.costo}, Ganancia: {self.ganancia} >'
