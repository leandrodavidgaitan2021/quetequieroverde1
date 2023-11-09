from flask import Blueprint, render_template, request, url_for, redirect, flash, g

# Importamos funcion para que que las vistas sea requerido logearse
from tienda.routers.auth import login_required, login_admin

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
        _categorias = categoria.Categoria.query.filter(categoria.Categoria.categoria.contains(q))
    else: 
        _categorias = categoria.Categoria.query.all()
    return render_template('categoria/lista.html', categorias = _categorias )



@bp.route('/crear', methods = ["GET", "POST"])
@login_required
@login_admin
def crear():
    if request.method == "POST":
        _categoria = request.form["categoria"]
        _creado_por = g.user.id

        categoria_ = categoria.Categoria(_categoria, _creado_por)
         
        busqueda_categoria = categoria.Categoria.query.filter_by(categoria = _categoria).first()
        
        if busqueda_categoria == None:
            db.session.add(categoria_)
            db.session.commit()
            return redirect(url_for('categorias.lista'))
        else:
            error = f'La categoria {_categoria} ya esta registrada'
            
        flash(error)
        
    return render_template('categoria/crear.html')


def get_categoria(id):
    categoria_buscada = categoria.Categoria.query.get_or_404(id)
    return categoria_buscada


@bp.route('/modificar/<int:id>', methods = ["GET", "POST"])
@login_required
@login_admin
def modificar(id):
    
    cate = get_categoria(id)
    
    if request.method == "POST":
        cate.categoria = request.form["categoria"]
        
        db.session.commit()
        
        return redirect(url_for('categorias.lista'))

    return render_template('categoria/modificar.html', cate = cate)

