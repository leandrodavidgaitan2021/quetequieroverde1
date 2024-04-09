from flask import Blueprint, render_template, request, url_for, redirect, flash, g

# Importamos funcion para que que las vistas sea requerido logearse
from tienda.routers.auth import login_required, login_admin
from tienda.routers.busquedas import * 

from tienda.modelos import categoria
from tienda import db


bp = Blueprint('categorias', __name__, url_prefix='/categorias')


# Todas las rutas y vistas
@bp.route('/lista')
@login_required
@login_admin
def lista():
    q = request.args.get('q')
    
    if q:
        _categorias = buscar_q_categorias(q)
    else: 
        _categorias = buscar_todas_categorias()
    return render_template('categoria/lista.html', categorias = _categorias )



@bp.route('/crear', methods = ["GET", "POST"])
@login_required
@login_admin
def crear():
    if request.method == "POST":
        _categoria = request.form["categoria"]
        _creado_por = g.user.id

        categoria_ = categoria.Categoria(_categoria, _creado_por)
         
        busqueda_categoria = buscar_categoria(_categoria)
        
        if busqueda_categoria == None:
            db.session.add(categoria_)
            db.session.commit()
            return redirect(url_for('categorias.lista'))
        else:
            error = f'La categoria {_categoria} ya esta registrada'
            
        flash(error)
        
    return render_template('categoria/crear.html')



@bp.route('/modificar/<int:id>', methods = ["GET", "POST"])
@login_required
@login_admin
def modificar(id):
    
    cate = buscar_id_categoria(id)
    
    if request.method == "POST":
        cate.categoria = request.form["categoria"]
        
        db.session.commit()
        
        return redirect(url_for('categorias.lista'))

    return render_template('categoria/modificar.html', cate = cate)

