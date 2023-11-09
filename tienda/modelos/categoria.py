from tienda import db

# Clase Categorias: contiene el id 
class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    categoria = db.Column(db.String(50), unique = True, nullable = False)
    creado_por = db.Column(db.Integer, nullable = False) 

    def __init__(self, categoria, creado_por):
        self.categoria = categoria
        self.creado_por = creado_por

    def __repr__(self):
        return f'<Categoria: {self.categoria} >'
