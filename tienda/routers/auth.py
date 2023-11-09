from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash

from tienda.modelos import user
from tienda import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

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
            return redirect(url_for('articulos.lista'))

        flash(error)
        
    return render_template('auth/login.html')


# Funcion para verificar si alguien inicio sesion
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = user.User.query.get_or_404(user_id)
        
@bp.route('logout')        
def logout():
    session.clear()
    return redirect(url_for('index'))

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
            return redirect(url_for('ventas.principal'))
        return view(**kwargs)
    return wrapped_view

    
