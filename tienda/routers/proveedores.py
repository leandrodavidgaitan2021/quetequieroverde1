from flask import Blueprint, render_template, request, url_for, redirect, flash, g

# Importamos funcion para que que las vistas sea requerido logearse
from tienda.routers.auth import login_required, login_admin
from tienda.routers.busquedas import * 

from tienda.modelos import proveedor
from tienda import db


bp = Blueprint('proveedores', __name__, url_prefix='/proveedores')


# Todas las rutas y vistas
@bp.route('/lista')
@login_required
@login_admin
def lista():
    q = request.args.get('q')
    
    if q:
        _proveedores = buscar_q_proveedores(q)
    else: 
        _proveedores = buscar_todos_proveedores()
    return render_template('proveedor/lista.html', proveedores = _proveedores )



@bp.route('/crear', methods = ["GET", "POST"])
@login_required
@login_admin
def crear():
    if request.method == "POST":
        _razonsocial = request.form["razonsocial"]
        _cuit = request.form["cuit"]
        _direccion = request.form["direccion"]
        _telefono = request.form["telefono"]
        _email = request.form["email"]
        _creado_por = g.user.id

        proveedor_ = proveedor.Proveedor(_razonsocial, _cuit, _direccion, _telefono, _email, _creado_por)
         
        busqueda_proveedor = buscar_razon_proveedores(_razonsocial)
        
        if busqueda_proveedor == None:
            db.session.add(proveedor_)
            db.session.commit()
            return redirect(url_for('proveedores.lista'))
        else:
            error = f'La Razon Social {_razonsocial} ya esta registrado'
            
        flash(error)
        
    return render_template('proveedor/crear.html')





@bp.route('/modificar/<int:id>', methods = ["GET", "POST"])
@login_required
@login_admin
def modificar(id):
    
    provee = buscar_id_proveedor(id)
    
    if request.method == "POST":
        provee.razonsocial = request.form["razonsocial"]
        provee.cuit = request.form["cuit"]
        provee.direccion = request.form["direccion"]
        provee.telefono = request.form["telefono"]
        provee.email = request.form["email"]
        
        db.session.commit()
        
        return redirect(url_for('proveedores.lista'))

    return render_template('proveedor/modificar.html', provee = provee)

