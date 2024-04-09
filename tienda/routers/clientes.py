from flask import Blueprint, render_template, request, url_for, redirect, flash, g

# Importamos funcion para que que las vistas sea requerido logearse
from tienda.routers.auth import login_required, login_admin
from tienda.routers.busquedas import *

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
        _clientes = buscar_q_clientes(q)
    else: 
        _clientes = buscar_todos_clientes()
        
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
         
        busqueda_cliente = buscar_nombre_clientes(_nombre)
        
        if busqueda_cliente == None:
            db.session.add(cliente_)
            db.session.commit()
            return redirect(url_for('clientes.lista'))
        else:
            error = f'La Razon Social {_nombre} ya esta registrado'
            
        flash(error)
        
    return render_template('cliente/crear.html')




@bp.route('/modificar/<int:id>', methods = ["GET", "POST"])
@login_required
@login_admin
def modificar(id):
    
    client = buscar_id_clientes(id)
    
    if request.method == "POST":
        client.nombre = request.form["nombre"]
        client.direccion = request.form["direccion"]
        client.telefono = request.form["telefono"]
        client.email = request.form["email"]
        
        db.session.commit()
        
        return redirect(url_for('clientes.lista'))

    return render_template('cliente/modificar.html', client = client)

