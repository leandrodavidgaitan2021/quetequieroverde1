from tienda import db

# Clase Articulo: con un id que es el numero de articulo, codart(puede ser codigo de barras o un entero)
class Articulo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    codart = db.Column(db.String(10), nullable = False)
    articulo = db.Column(db.String(20), nullable = False)
    descripcion = db.Column(db.String(50))
    descripcion_larga = db.Column(db.String(750))
    tipo = db.Column(db.String(20), nullable = False)
    costo = db.Column(db.Integer, nullable = False)
    precio = db.Column(db.Integer, nullable = False)
    stock = db.Column(db.Integer, nullable = False)
    proveedor = db.Column(db.String(50), nullable = False)
    imgfile = db.Column(db.String(255))
    creado_por = db.Column(db.Integer, nullable = False) 
    
    
    def __init__(self, codart, articulo, descripcion, descripcion_larga, tipo, costo, precio, stock, proveedor, imgfile, creado_por):
        self.codart = codart
        self.articulo = articulo
        self.descripcion = descripcion
        self.descripcion_larga = descripcion_larga     
        self.tipo = tipo
        self.costo = costo
        self.precio = precio
        self.stock = stock
        self.proveedor = proveedor
        self.imgfile = imgfile
        self.creado_por = creado_por

        
    def __repr__(self):
        return f'<Articulo: {self.articulo} >'
