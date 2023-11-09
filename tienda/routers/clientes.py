from flask import Blueprint, render_template, request, url_for, redirect, flash, g

# Importamos funcion para que que las vistas sea requerido logearse
from tienda.routers.auth import login_required, login_admin

from tienda.modelos import cliente
from tienda import db


bp = Blueprint('clientes', __name__, url_prefix='/clientes')


# Todas las rutas y vistas
@bp.route('/lista')
@login_required
@login_admin
def lista():
    q = request.args.get('q')
    
    if q:
        _clientes = cliente.Cliente.query.filter(cliente.Cliente.nombre.contains(q))
    else: 
        _clientes = cliente.Cliente.query.all()
    return render_template('cliente/lista.html', clientes = _clientes )

@bp.route('/crear', methods = ["GET", "POST"])
@login_required
@login_admin
def crear():
    if request.method == "POST":
        _nombre = request.form["nombre"]
        _direccion = request.form["direccion"]
        _telefono = request.form["telefono"]
        _email = request.form["email"]


        cliente_ = cliente.Cliente(_nombre, _direccion, _telefono, _email)
         
        busqueda_proveedor = cliente.Cliente.query.filter_by(nombre = _nombre).first()
        
        if busqueda_proveedor == None:
            db.session.add(cliente_)
            db.session.commit()
            return redirect(url_for('clientes.lista'))
        else:
            error = f'La Razon Social {_nombre} ya esta registrado'
            
        flash(error)
        
    return render_template('cliente/crear.html')


def get_cliente(id):
    cliente_buscado = cliente.Cliente.query.get_or_404(id)
    return cliente_buscado


@bp.route('/modificar/<int:id>', methods = ["GET", "POST"])
@login_required
@login_admin
def modificar(id):
    
    client = get_cliente(id)
    
    if request.method == "POST":
        client.nombre = request.form["nombre"]
        client.direccion = request.form["direccion"]
        client.telefono = request.form["telefono"]
        client.email = request.form["email"]
        
        db.session.commit()
        
        return redirect(url_for('clientes.lista'))

    return render_template('cliente/modificar.html', client = client)

