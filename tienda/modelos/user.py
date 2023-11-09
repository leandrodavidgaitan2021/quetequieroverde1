from tienda import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    password = db.Column(db.Text, nullable = False)
    apellido = db.Column(db.String(40))
    nombre = db.Column(db.String(40))
    cuit = db.Column(db.String(12))
    tcliente = db.Column(db.String(40))
    direccion = db.Column(db.String(60))
    telefono = db.Column(db.String(40))
    email = db.Column(db.String(40))
    fechanac = db.Column(db.String(40))
    
    def __init__(self, username, password, apellido, nombre, cuit, tcliente, direccion, telefono, email, fechanac):
        self.username = username
        self.password = password
        self.apellido = apellido
        self.nombre = nombre
        self.cuit = cuit
        self.tcliente = tcliente
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.password = password
        self.fechanac = fechanac
        
    def __repr__(self):
        return f'<User: {self.username} >'
