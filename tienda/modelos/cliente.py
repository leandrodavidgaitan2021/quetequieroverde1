from tienda import db

# Clase Cliente: contiene el id que se relaciona con codigo de proveedor
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50), unique = True, nullable = False)
    direccion = db.Column(db.String(50), nullable = False)
    telefono = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(50), nullable = False)

    def __init__(self, nombre, direccion, telefono, email):
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email


    def __repr__(self):
        return f'{self.nombre}'