from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from tienda.routers.busquedas import * 
from tienda.modelos import user
from tienda import db

bp = Blueprint('auth', __name__, url_prefix='/auth')


# Para que no se pueda ingresar alguna pagina sin loguearse
import functools
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


def login_admin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user.tcliente != "Administrador":
            return redirect(url_for('ventas.lista'))
        return view(**kwargs)
    return wrapped_view


# RUTA QUE CIERRA LA SECCION    
@bp.route('logout')  
@login_required      
def logout():
   
    session.clear()

    return redirect(url_for('index'))



# Funcion para verificar si alguien inicio sesion
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = user.User.query.get_or_404(user_id)
        







# RUTA QUE REALIZA EL REGISTRO DEL USUARIO
@bp.route('/register', methods = ["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        apellido = request.form["apellido"]
        nombre = request.form["nombre"]
        cuit = request.form["cuit"]
        tcliente = request.form["tcliente"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]
        email = request.form["email"]
        fechanac = request.form["fechanac"]

        usuario = user.User(username, generate_password_hash(password), apellido, nombre, cuit, tcliente,direccion, telefono, email, fechanac)
        
        user_name = user.User.query.filter_by(username = username).first()
        
        if user_name == None:
            db.session.add(usuario)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            error = f'El usuario {username} ya esta registrado'
            
        flash(error)
        
    return render_template('auth/register.html')



# RUTA QUE REALIZA EL LOGIN DEL USUARIO
@bp.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
    
        error = None
        # Validar datos
      
        usuario_db = user.User.query.filter_by(username = username).first()
        
        if usuario_db == None:
            error = 'Nombre de usuario incorrecto'
        elif not check_password_hash(usuario_db.password, password):
            error = 'Contraseña incorrecto'

        # Iniciar sesion
        if error is None:
            session.clear()
            session['user_id'] = usuario_db.id
            if usuario_db.tcliente == "Administrador":
                return redirect(url_for('articulos.lista'))
            else:
                return redirect(url_for('pedidos.principal'))

        flash(error)
        
    return render_template('auth/login.html')


# RUTA QUE CAMBIA LA CLAVE DEL USUARIO
@bp.route('/cambiar_clave', methods = ["GET", "POST"])
@login_required
@login_admin
def cambiar_clave():

    if request.method == "POST":
        datos = request.json
        clave_vieja = datos['claveVieja']
        clave_nueva = datos['claveNueva']

        # Lógica para verificar la clave vieja y cambiarla
        if verificar_clave_vieja(clave_vieja):
            cambiar_clave_en_la_base_de_datos(clave_nueva)
            # Cerrar la sesión después de cambiar la contraseña
            #session.clear()
            logout()
            return jsonify({'mensaje': 'Contraseña cambiada con éxito.'})
        else:
            return jsonify({'mensaje': 'Error: La contraseña vieja no es correcta.'}), 400
        
    return render_template('auth/cambiar_clave.html')



# RUTA QUE REALIZA EL REGISTRO DE ADMINISTRADOR
@bp.route('/crear_administrador', methods = ["GET", "POST"])
def crear_administrador():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        apellido = request.form["apellido"]
        nombre = request.form["nombre"]
        cuit = request.form["cuit"]
        tcliente = "Administrador"
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]
        email = request.form["email"]
        fechanac = request.form["fechanac"]

        usuario = user.User(username, generate_password_hash(password), apellido, nombre, cuit, tcliente,direccion, telefono, email, fechanac)
        
        user_name = user.User.query.filter_by(username = username).first()
        
        if user_name == None:
            db.session.add(usuario)
            db.session.commit()
            error = f'El usuario {username} se registro CORRECTAMENTE'
            #return redirect(url_for('articulos.lista'))
        else:
            error = f'El usuario {username} ya esta registrado'
            
        flash(error)
        
    return render_template('auth/register.html')


# RUTA QUE MUESTRA LAS OPCIONES QUE TIENE EL ADMINISTRADOR
@bp.route('/opciones')
@login_required
@login_admin
def opciones():
       
    return render_template('auth/opciones.html')




def verificar_clave_vieja(clave_vieja):
    id = g.user.id
    usuario = buscar_id_usurio(id)
    return check_password_hash(usuario.password, clave_vieja)

                


def cambiar_clave_en_la_base_de_datos(clave_nueva):
    id = g.user.id
    usuario = buscar_id_usurio(id)
    usuario.password = generate_password_hash(clave_nueva)
    db.session.commit()




        
        
