from flask import Blueprint, render_template, request, url_for, redirect, flash, g, jsonify, json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

# Importamos funcion para que que las vistas sea requerido logearse
from tienda.routers.auth import login_required, login_admin
from tienda.routers.busquedas import *


from tienda.modelos import caja
from tienda import db


bp = Blueprint('cajas', __name__, url_prefix='/cajas')

#unidad_local = '/home/leandrodavidgaitan2021/quetequieroverde1/tienda/static/pdf/'
unidad_local = 'e:/quetequieroverde/tienda/static/pdf/'

#unidad_local_pdf = '/home/leandrodavidgaitan2021/quetequieroverde1/tienda/static/'
unidad_local_pdf = 'e:/quetequieroverde/tienda/static/'

# Lista los productos antes de logearse
@bp.route('/ver_caja', methods = ["GET", "POST"])
@login_admin
@login_required
def ver_caja():

    _fecha_actual = fecha_a_mostrar(fecha_actual())
    # se toma id usuario
    _id = g.user.id
   

    # se guardan todas las cajas por id usuario = creado_por
    _cajas = caja.Caja.query.order_by(caja.Caja.id.desc()).filter(caja.Caja.creado_por.contains(_id)).all()

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
    return render_template('caja/caja.html', 
                           t_e_compra = total_compra_efectivo, 
                           t_b_compra = total_compra_billetera,
                           t_e_venta = total_venta_efectivo, 
                           t_b_venta = total_venta_billetera,
                           t_transf_a_efectivo = total_transferencia_a_efectivo,
                           t_transf_a_billetera = total_transferencia_a_billetera, 
                           fecha = _fecha_actual
                           )


# Lista los productos antes de logearse
@bp.route('/lista', methods = ["GET", "POST"])
@login_admin
@login_required
def lista():
    # fecha actual
    _fecha_actual = fecha_a_mostrar(fecha_actual())
    # se toma id usuario
    id = g.user.id

    # se guardan todas las cajas por id usuario = creado_por
    _cajas = caja.Caja.query.order_by(caja.Caja.id.desc()).filter(caja.Caja.creado_por.contains(id)).all()


                        
    # se envia todo a la pagina
    return render_template('caja/lista.html', 
                           cajas = _cajas, 
                           fecha = _fecha_actual
                           )




@bp.route('/transferencia', methods = ["GET", "POST"])
@login_required
@login_admin
def transferencia():
    # fecha actual
    fecha_actual = fecha_hora_actual()
    if request.method == "POST":
        datos = request.json
        _fecha = datos['fecha'] # Datos del lado del cliente, fecha seleccionado
        _fecha = guarda_fecha(_fecha)
        tipo_moviento = datos['opcion']  # Datos del lado del cliente, tipo movimiento
        monto = datos['monto'] # Datos del lado del cliente, monto

        _tipo = "T"
        _id_tipo = 0
        _monto = int(monto)
        _creado_por = g.user.id
        
        if tipo_moviento == "A EFECTIVO":
            _caja = "E"
            caja_ = caja.Caja(_fecha, _tipo, _id_tipo, _caja, _monto, _creado_por)
            db.session.add(caja_)
            db.session.commit()    
            return jsonify({'mensaje': 'Transferencia realizada con éxito.'})
        
        elif tipo_moviento == "A BILLETERA":
            _caja = "B"
            caja_ = caja.Caja(_fecha, _tipo, _id_tipo, _caja, _monto, _creado_por)
            db.session.add(caja_)
            db.session.commit()    
            return jsonify({'mensaje': 'Transferencia realizada con éxito.'})

    return render_template('caja/transferencia.html', fecha = fecha_actual)


#Genera pdf


def generate_pdf(operacion, detalles, aquien):
    _tipo = ''
    _caja = ''
    _quien = ''
    _nombre = ''

    vendedor = ''
    if operacion.caja == "B": 
        _caja = 'Billetera'
    if operacion.caja == "E": 
        _caja = 'Efectivo'

        
    if operacion.tipo == "C": # Compra
        pdf_filename = f'compra-{operacion.id}-{operacion.fecha}.pdf'
        _tipo = 'Compra'
        _quien = 'Proveedor'
        _nombre = aquien.razonsocial
        _vendedor = _nombre
    if operacion.tipo == "V": # Compra
        pdf_filename = f'venta-{operacion.id}-{operacion.fecha}.pdf'
        _tipo = 'Venta'
        _quien = 'Cliente'
        _nombre = aquien.nombre

    if operacion.tipo == "T":
        pdf_filename = f'transferencia-{operacion.id}-{operacion.fecha}.pdf'
        _tipo = 'Transferencia'
        _quien = 'Caja'
        _nombre = aquien.username

        
    pdf_mostrar = 'pdf/'+ pdf_filename 
    pdf_filename = unidad_local + pdf_filename
    x = 30
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    y = 750
    c.drawString(x, y, f"Que Te Quiero Verde - Resumen Operación")
    y -= 30
    c.drawString(x, y, f"Fecha: {operacion.fecha}")
    y -= 20
    c.drawString(x, y, f"Tipo: {_tipo}")
    y -= 20
    c.drawString(x, y, f"Caja: {_caja}")
    y -= 20
    c.drawString(x, y, f"{_quien}: {_nombre}")
   
    y -= 20
    c.drawString(x, y, f"-----------------------------------------------------------------------------------------------------------------------------")
    y -= 20
    if operacion.tipo != "T":
        c.drawString(x+20, y, f"Articulo")
        c.drawString(x+250, y, f"Cantidad")
        c.drawString(x+350, y, f"Precio")
        c.drawString(x+450, y, f"Subtotal")
        y -= 30
        for detalle in detalles:

            c.drawString(x+20, y, f'{detalle["articulo"]}')
            c.drawString(x+270, y, f'{detalle["cantidad"]}')
            c.drawString(x+350, y, f'$ {detalle["precio"]}')
            c.drawString(x+450, y, f'$ {detalle["precio"] * detalle["cantidad"]}')
            y -= 20
    else:
        c.drawString(x+50, y, f"{detalles}")
    y -= 50
    c.drawString(x+420, y, f"Total: $ { operacion.monto}")
    
    c.save()
        
    return vendedor, pdf_mostrar





@bp.route('/ver_operacion/<int:id>', methods = ["GET"])
@login_required
@login_admin
def ver_operacion(id):
#    print(id)
    operacion = buscar_operacion(id)
#    print(operacion)
    
    if operacion.tipo == "C":
        aquien, detalles = get_compra(operacion.id_tipo)
    if operacion.tipo == "V":
        aquien, detalles = get_venta(operacion.id_tipo)

        
        
    if operacion.tipo == "T":
        if operacion.caja == "E":
            detalles = f"El dia {operacion.fecha}, se transfirio de Billetera a Efectivo, ${operacion.monto}"
        if operacion.caja == "B":
            detalles = f"El dia {operacion.fecha}, se transfirio de Efectivo a Billetera, ${operacion.monto}"
        aquien = buscar_id_usuario(operacion.creado_por)
 
        

    vendedor, archivo_pdf = generate_pdf(operacion, detalles, aquien)
 
      
    return render_template('caja/ver_operacion.html', archivo_pdf = archivo_pdf, aquien = aquien, vendedor = vendedor)


@bp.route('/eliminar', methods=['POST'])
@login_admin
@login_required
def eliminar():
    data = request.json

    nombre_pdf = data['nombre_pdf']
    print(nombre_pdf)

    nombre_pdf = unidad_local_pdf + nombre_pdf
    print(nombre_pdf)
    
    eliminar_pdf(nombre_pdf)

    return jsonify({'message': 'PDF eleminado con éxito'})

def eliminar_pdf(nombre_pdf):
    os.remove(nombre_pdf)