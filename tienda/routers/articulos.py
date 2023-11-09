from flask import Blueprint, render_template, request, url_for, redirect, flash, g, session
import re

# Importamos funcion para que que las vistas sea requerido logearse
from tienda.routers.auth import login_required, login_admin

from tienda.modelos import articulo, proveedor, categoria, actualizacion
from tienda import db


bp = Blueprint('articulos', __name__, url_prefix='/articulos')




# Todas las rutas y vistas
@bp.route('/lista')
@login_required
@login_admin
def lista():
    q = request.args.get('q')
    
    if q:
        _articulos = articulo.Articulo.query.filter(
            articulo.Articulo.articulo.contains(q) | 
            articulo.Articulo.codart.contains(q) |
            articulo.Articulo.proveedor.contains(q) |
            articulo.Articulo.tipo.contains(q))
    else:   
        _articulos = articulo.Articulo.query.all()
    return render_template('articulo/lista.html', articulos = _articulos)


@bp.route('/crear', methods = ["GET", "POST"])
@login_required
@login_admin
def crear():

    proveedores = proveedor.Proveedor.query.all()
    categorias = categoria.Categoria.query.all()
    listacodigo = []

    for cate in categorias:
        if cate.categoria != "Gastos":
            letra_a_buscar = cate.categoria[0]
                
            # Realiza una consulta SQL para obtener el último código de artículo que coincide con la letra
            ultimo_codigo = db.session.query(articulo.Articulo.codart).filter(articulo.Articulo.codart.like(f'{letra_a_buscar}%')).order_by(articulo.Articulo.id.desc()).first()

            ultimo = str(ultimo_codigo)
            ultimo = extraer_valor_entre_delimitadores(letra_a_buscar , ultimo)
        
            if ultimo:
                listacodigo.append(ultimo)


    
    if request.method == "POST":
        _codart = request.form["codigoart"]
        _articulo = request.form["articulo"]
        _descripcion = ""
        _descripcion_larga = ""
        _tipo = request.form["tipo"]
        _costo = int(request.form["costo"])
        _precio = int(request.form["precio"])
        _stock = 0
        _proveedor = request.form["proveedor"]
        _imgfile = ""
        _creado_por = g.user.id

        articulo_ = articulo.Articulo(
            _codart, 
            _articulo,
            _descripcion,
            _descripcion_larga, 
            _tipo, 
            _costo, 
            _precio,
            _stock, 
            _proveedor,
            _imgfile, 
            _creado_por)
       
        busqueda_articulo = articulo.Articulo.query.filter_by(codart = _codart).first()
        
        if busqueda_articulo == None:
            db.session.add(articulo_)
            db.session.commit()
            return redirect(url_for('articulos.lista'))
        else:
            error = f'El codigo de articulo {_codart} ya esta registrado'
            
        flash(error)

    return render_template('articulo/crear.html', proveedores = proveedores, categorias = categorias, listacodi = listacodigo)




@bp.route('/modificar/<int:id>', methods = ["GET", "POST"])
@login_required
@login_admin
def modificar(id):
    
    art = get_articulo(id)
    
    if request.method == "POST":
        art.articulo = request.form["articulo"]
        #art.descripcion = request.form["descripcion"]
        #art.descripcion_larga = request.form["descripcion_larga"]
        art.costo = int(request.form["costo"])
        art.precio = int(request.form["precio"])
        #art.imgfile = request.form["imgfile"]
        db.session.commit()
        
        return redirect(url_for('articulos.lista'))

    return render_template('articulo/modificar.html', art = art)




def get_articulo(id):
    articulo_buscado = articulo.Articulo.query.get_or_404(id)
    return articulo_buscado




def extraer_valor_entre_delimitadores(letra, cadena):
    inicio = f"('{letra}"
    fin = "',)"

    # Utilizamos una expresión regular para buscar el valor entre los delimitadores
    patron = re.escape(inicio) + r'(.*?)' + re.escape(fin)
    resultado = re.search(patron, cadena)

    if resultado:
        valor_entre_delimitadores = resultado.group(1)
        valor_entre_delimitadores = int(valor_entre_delimitadores) + 1
        valor_entre_delimitadores = str(valor_entre_delimitadores)
        valor_entre_delimitadores = f"{letra}{valor_entre_delimitadores}"

    else:
        valor_entre_delimitadores = f"{letra}1"
    return valor_entre_delimitadores   

          
          
@bp.route('actualizar/', methods = ["GET", "POST"])
@login_required
@login_admin
def actualizar():

    proveedores = proveedor.Proveedor.query.all()
    categorias = categoria.Categoria.query.all()
    
    if request.method == "POST":
        _proveedor = request.form["proveedor"]
        _tipo = request.form["tipo"]
        _porcentaje = int(request.form["porcentaje"])
        _creado_por = g.user.id

        actualizacion_ = actualizacion.Actualizacion(
            _proveedor,
            _tipo, 
            _porcentaje,
            _creado_por)
        
        if _proveedor == "Todos" and _tipo == "Todos":
            todos_articulo = articulo.Articulo.query.all()
        elif _proveedor == "Todos" and _tipo != "Todos":
            todos_articulo = articulo.Articulo.query.filter_by(tipo = _tipo).all()
        elif _proveedor != "Todos" and _tipo == "Todos":
            todos_articulo = articulo.Articulo.query.filter_by(proveedor = _proveedor).all()
        elif _proveedor != "Todos" and _tipo != "Todos":
            todos_articulo = articulo.Articulo.query.filter_by(and_(proveedor = _proveedor, tipo = _tipo)).all()
            
        for _articulo in todos_articulo:
            _articulo.precio = int(_articulo.precio * ((_porcentaje/100) + 1))
        
   
        db.session.add(actualizacion_)
        db.session.commit()

    return render_template('articulo/actualizar.html', proveedores = proveedores, categorias = categorias)