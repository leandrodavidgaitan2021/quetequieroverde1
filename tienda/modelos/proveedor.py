from tienda import db

# Clase Proveedores: contiene el id que se relaciona con codigo de proveedor
class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    razonsocial = db.Column(db.String(50), unique = True, nullable = False)
    cuit = db.Column(db.String(12), unique = True, nullable = False)
    direccion = db.Column(db.String(50), nullable = False)
    telefono = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(50), nullable = False)
    creado_por = db.Column(db.Integer, nullable = False) 

    def __init__(self, razonsocial, cuit, direccion, telefono, email, creado_por):
        self.razonsocial = razonsocial
        self.cuit = cuit
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.creado_por = creado_por

    def __repr__(self):
        return f'{self.razonsocial}'
