from flask import Blueprint, render_template, request, url_for, redirect, flash, g, jsonify, json
from datetime import datetime

# Importamos funcion para que que las vistas sea requerido logearse
from tienda.routers.auth import login_required, login_admin



from tienda.modelos import caja
from tienda import db


bp = Blueprint('cajas', __name__, url_prefix='/cajas')



# Lista los productos antes de logearse
@bp.route('/lista', methods = ["GET", "POST"])
@login_required
def lista():
    # fecha actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    # se toma id usuario
    id = g.user.id
   

    # se guardan todas las cajas por id usuario = creado_por
    _cajas = caja.Caja.query.filter(caja.Caja.creado_por.contains(id))
    
    # se inicializan las variales totales
    total_compra_efectivo = 0
    total_compra_billetera = 0
    total_venta_efectivo = 0
    total_venta_billetera = 0
    total_transferencia_a_efectivo = 0
    total_transferencia_a_billetera = 0
     
    # se busca los tipo de ventas y se guarda por tipo de caja el monto   
    for _caja in _cajas:
        if _caja.tipo == "V":
            if _caja.caja == "E":
                total_venta_efectivo += _caja.monto
            if _caja.caja == "B":
                total_venta_billetera += _caja.monto
        elif _caja.tipo == "C":
            if _caja.caja == "E":
                total_compra_efectivo += _caja.monto
            if _caja.caja == "B":
                total_compra_billetera += _caja.monto
        elif _caja.tipo == "T":
            if _caja.caja == "E":
                total_transferencia_a_efectivo += _caja.monto
            if _caja.caja == "B":
                total_transferencia_a_billetera += _caja.monto
           
                        
    # se envia todo a la pagina
    return render_template('caja/lista.html', 
                           cajas = _cajas, 
                           t_e_compra = total_compra_efectivo, 
                           t_b_compra = total_compra_billetera,
                           t_e_venta = total_venta_efectivo, 
                           t_b_venta = total_venta_billetera,
                           t_transf_a_efectivo = total_transferencia_a_efectivo,
                           t_transf_a_billetera = total_transferencia_a_billetera, 
                           fecha = fecha_actual
                           )



@bp.route('/transferir', methods = ["GET", "POST"])
@login_required
def transferir():
    # Obtiene los datos enviados desde el cliente
    data = request.get_json()  
    _fecha = data['fecha'] # Datos del lado del cliente, fecha seleccionado
    _fecha = datetime.strptime(_fecha, "%Y-%m-%d").date()
    tipo_moviento = data['opcion']  # Datos del lado del cliente, tipo movimiento
    monto = data['monto'] # Datos del lado del cliente, monto

    
    if tipo_moviento == "A EFECTIVO":
        tipo_ = "T"
        caja_ = "E"
        monto_ = int(monto)
        creado_por_ = g.user.id
        caja_ = caja.Caja(_fecha, tipo_, caja_, monto_, creado_por_)
        db.session.add(caja_)
        db.session.commit()
    elif tipo_moviento == "A BILLETERA":
        tipo_ = "T"
        caja_ = "B"
        monto_ = int(monto)
        creado_por_ = g.user.id
        caja_ = caja.Caja(_fecha, tipo_, caja_, monto_, creado_por_)
        db.session.add(caja_)
        db.session.commit()

     
    return redirect(url_for('cajas.lista'))