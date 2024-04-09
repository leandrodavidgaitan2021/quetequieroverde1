from flask import Blueprint, render_template, request, url_for, redirect, flash, g

# Importamos funcion para que que las vistas sea requerido logearse
from tienda.routers.auth import login_required, login_admin

from tienda.modelos import cliente
from tienda import db


bp = Blueprint('ubicaciones', __name__, url_prefix='/ubicacion')



# Todas las rutas y vistas
@bp.route('/ubicar')
@login_required
@login_admin
def ubicar():
        return render_template('ubicacion/ubicar.html')


@bp.route('/procesar_formulario', methods=['POST'])
def procesar_formulario():
        

    imagen_seleccionada = request.files['imagen']
    imagen_camara = request.form['imagen-camara']

    # Aquí puedes realizar cualquier acción adicional con los datos recibidos

    return f'Imagen Seleccionada: {imagen_seleccionada.filename}, Imagen desde Cámara: {imagen_camara}'
