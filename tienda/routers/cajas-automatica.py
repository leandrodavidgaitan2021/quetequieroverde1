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
    
    _caja_ = realizar_caja()
    
    return _caja_  




def realizar_caja():
    from tienda.modelos import  venta, detalle_venta, compra, detalle_compra
    
    ventas_ = venta.Venta.query.all()
   
    for venta_ in ventas_:
        id_ = venta_.id
        fecha_venta_ = venta_.fecha
        tipo_ = "V"
        caja_ = venta_.metodo_pago
        monto_ = 0
        creado_por_ = venta_.creado_por
        
        # print(f"ID VENTA: {id_}")
        # print(f"FECHA VENTA: {fecha_venta_}")
        # print(f"TIPO VENTA: {tipo_}")
        # print(f"CAJA VENTA: {caja_}")
        # print(f"MONTO VENTA cero: {monto_}")
        # print(f"CREADO POR VENTA: {creado_por_}")
        
        detalle_ventas_ = detalle_venta.DetalleVenta.query.filter_by(venta_id = id_).all()
        for detalle_venta_ in detalle_ventas_:
            # print(f"ID DETALLE VENTA: {detalle_venta_.id}")
            # print(f"ID VENTA: {detalle_venta_.venta_id}")
            # print(f"ID ARTICULO VENTA: {detalle_venta_.articulo_id}")
            # print(f"CANTIDAD VENTA: {detalle_venta_.cantidad}")
            # print(f"PRECIO U VENTA: {detalle_venta_.precio_unitario}")
            # print(monto_)
            monto_ += (detalle_venta_.cantidad * detalle_venta_.precio_unitario)
            # print(monto_)
        
        _caja = caja.Caja(fecha_venta_, tipo_, caja_, monto_, creado_por_)
        db.session.add(_caja)
        db.session.commit()


    compras_ = compra.Compra.query.all()

    for compra_ in compras_:
        id_ = compra_.id
        fecha_compra_ = compra_.fecha
        tipo_ = "C"
        caja_ = compra_.metodo_pago
        monto_ = 0
        creado_por_ = compra_.creado_por
        
        detalle_compras_ = detalle_compra.DetalleCompra.query.filter_by(compra_id = id_).all()
        for detalle_compra_ in detalle_compras_:
            monto_ += (detalle_compra_.cantidad * detalle_compra_.precio_unitario)
        
        _caja = caja.Caja(fecha_compra_, tipo_, caja_, monto_, creado_por_)
        db.session.add(_caja)
        db.session.commit()

    
    return "Se realizo caja"



