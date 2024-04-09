from flask import Blueprint, render_template, request, url_for, redirect, flash, g, session
from PIL import Image
import os
import re

# Importamos funcion para que que las vistas sea requerido logearse
from tienda.routers.auth import login_required, login_admin
from tienda.routers.busquedas import * 

from tienda.modelos import articulo, proveedor, categoria, actualizacion
from tienda import db


bp = Blueprint('articulos', __name__, url_prefix='/articulos')

#unidad_local = '/home/leandrodavidgaitan2021/quetequieroverde1/tienda/static/uploads/productos-imagenes/'
unidad_local = 'e:/quetequieroverde/tienda/static/uploads/productos-imagenes/'
unidad_ddb = 'uploads/productos-imagenes/'



# Todas las rutas y vistas
@bp.route('/lista')
@login_required
@login_admin
def lista():
    q = request.args.get('q')
    
    if q:
        _articulos = buscar_articulos(q)
    else:   
        _articulos = buscar_todos_articulos()
    return render_template('articulo/lista.html', articulos = _articulos)


@bp.route('/crear', methods = ["GET", "POST"])
@login_required
@login_admin
def crear():

    proveedores = buscar_todos_proveedores()
    categorias = buscar_todas_categorias()
    
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
        _codart = request.form["codart"]
        _articulo = request.form["articulo"]
        _descripcion = ""
        _descripcion_larga = ""
        _tipo = request.form["tipo"]
        _costo = 0
        _precio = 0
        _stock = 0
        _proveedor = request.form["proveedor"]
        _imgfile = ""
        _creado_por = g.user.id

        article_image = request.files['articleImage']  # toma la imagen
        
        # Verifica si el formulario tiene un archivo adjunto
        if article_image.filename != '':

            file_extension = article_image.filename.rsplit('.', 1)[-1]  #captura la extension del archivo

            article_image.filename = _codart +"."+ file_extension  # Cambia el nombre de la imagen

            _imgfile = unidad_ddb + article_image.filename  # Coloca dirrecion imagen para guardar en bbdd
            imgfilecompleto = unidad_local + article_image.filename  # Coloca dirrecion imagen completa para guardar

            img = Image.open(article_image)

            # Ajusta la orientación de la imagen si tiene información EXIF
            if tiene_info_exif(img):
                img = corregir_orientacion(img)

            # Redimensiona la imagen manteniendo la proporción
            #img.thumbnail((250, 250))

            # Redimensiona la imagen
            img = img.resize((250, 250))

            img.save(imgfilecompleto)
            
       
        #busqueda_articulo = articulo.Articulo.query.filter_by(codart = _codart).first()
        busqueda_articulo = buscar_cod_articulo(_codart)
        
        if busqueda_articulo == None:
            
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
            
            db.session.add(articulo_)
            db.session.commit()
            
            error = f'El articulo de codigo: {_codart}, se creo correctamente registrado'
            flash(error)
            return redirect(url_for('articulos.crear'))
        else:
            error = f'El codigo de articulo {_codart} ya esta registrado'
            flash(error)

    return render_template('articulo/crear.html', proveedores = proveedores, categorias = categorias, listacodi = listacodigo)




@bp.route('/modificar/<int:id>', methods = ["GET", "POST"])
@login_required
@login_admin
def modificar(id):
    
    #art = get_articulo(id)
    art = buscar_id_articulo(id)
    
    if request.method == "POST":
        _imgfile = art.imgfile

        article_image = request.files['articleImage']  # toma la imagen
        
        # Verifica si el formulario tiene un archivo adjunto
        if article_image.filename != '':

            file_extension = article_image.filename.rsplit('.', 1)[-1]  #captura la extension del archivo

            article_image.filename = art.codart +"."+ file_extension  # Cambia el nombre de la imagen

            _imgfile = unidad_ddb + article_image.filename  # Coloca dirrecion imagen para guardar en bbdd
            imgfilecompleto = unidad_local + article_image.filename  # Coloca dirrecion imagen completa para guardar
            
            
            img = Image.open(article_image)

            # Ajusta la orientación de la imagen si tiene información EXIF
            if tiene_info_exif(img):
                img = corregir_orientacion(img)

            # Redimensiona la imagen manteniendo la proporción
            #img.thumbnail((250, 250))

            # Redimensiona la imagen
            img = img.resize((250, 250))

            img.save(imgfilecompleto)
        
           
        art.articulo = request.form["articulo"]
        #art.descripcion = request.form["descripcion"]
        #art.descripcion_larga = request.form["descripcion_larga"]
        art.costo = int(request.form["costo"])
        art.precio = int(request.form["precio"])
        art.imgfile = _imgfile
        db.session.commit()
        error = f'El articulo de codigo: {art.codart}, se modifico correctamente registrado'
        flash(error)
        return render_template('articulo/modificar.html', art = art)
    
#    flash(error)

    return render_template('articulo/modificar.html', art = art)



      



#  METODO DE ACTUALIZAR PRECIOS          
@bp.route('actualizar/', methods = ["GET", "POST"])
@login_required
@login_admin
def actualizar():
    #busca todos los proveedores
    # proveedores = proveedor.Proveedor.query.all()
    # categorias = categoria.Categoria.query.all()
    proveedores = buscar_todos_proveedores()
    categorias = buscar_todas_categorias()
    
    if request.method == "POST":
        _proveedor = request.form["proveedor"]
        _tipo = request.form["tipo"]
        _costo = int(request.form["costo"])
        _ganancia = int(request.form["ganancia"])
        _creado_por = g.user.id

        actualizacion_ = actualizacion.Actualizacion(
            _proveedor,
            _tipo, 
            _costo,
            _ganancia,
            _creado_por)
        
        if _proveedor == "Todos" and _tipo == "Todos":
            todos_articulo = buscar_todos_articulos()
        elif _proveedor == "Todos" and _tipo != "Todos":
            todos_articulo = buscar_tipo_articulo(_tipo)
        elif _proveedor != "Todos" and _tipo == "Todos":
            todos_articulo = buscar_proveedor_articulo(_proveedor)
        elif _proveedor != "Todos" and _tipo != "Todos":
            todos_articulo = buscar_todos_provee_tipo_articulos(_proveedor, _tipo)
            
        for _articulo in todos_articulo:
            print(f"Costo: {_articulo.costo}")
            print(f"Precio: {_articulo.precio}")
            if _costo != 0:
                _articulo.costo = int(_articulo.costo * ((_costo/100) + 1))
                if _ganancia != 0:
                    _articulo.precio = int(_articulo.costo * ((_ganancia/100) + 1))
            elif _ganancia != 0:
                _articulo.precio = int(_articulo.precio * ((_ganancia/100) + 1))
                
                
            print(f"Costo + {_costo}: {_articulo.costo}")
            print(f"Precio + {_ganancia}: {_articulo.precio}")
            
        db.session.add(actualizacion_)
        db.session.commit()

    return render_template('articulo/actualizar.html', proveedores = proveedores, categorias = categorias)





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

def tiene_info_exif(imagen):
    try:
        # Intenta extraer la orientación de la imagen
        orientacion = imagen._getexif().get(274)
        return orientacion is not None

    except (AttributeError, KeyError, IndexError):
        # Si hay algún error al intentar acceder a los metadatos EXIF, se asume que no hay información
        return False

def corregir_orientacion(imagen):
    try:
        # Extrae la orientación de la imagen
        orientacion = imagen._getexif().get(274)
        print(orientacion)

        # Aplica una rotación según la orientación
        if orientacion == 3:
            imagen = imagen.rotate(180, expand=True)
        elif orientacion == 6:
            imagen = imagen.rotate(270, expand=True)
        elif orientacion == 8:
            imagen = imagen.rotate(90, expand=True)

    except (AttributeError, KeyError, IndexError):
        # En caso de error, simplemente continúa sin modificar la orientación
        pass

    return imagen 