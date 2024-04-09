from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy



# create the extension
db = SQLAlchemy()


def create_app():
    
    app= Flask(__name__)

    
    # Configuracion del proyecto
    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = 'dev',
        # configure the SQLite database, relative to the app instance folder
        SQLALCHEMY_DATABASE_URI = "sqlite:///tienda.db"
    )
    
    
    # initialize the app with the extension
    db.init_app(app)

    # Registrar Blueprint
    from .routers import auth, proveedores, categorias, clientes, ventas, compras, cajas, pedidos, ubicaciones, articulos
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(articulos.bp)
    app.register_blueprint(proveedores.bp)
    app.register_blueprint(categorias.bp)
    app.register_blueprint(clientes.bp)
    app.register_blueprint(ventas.bp)
    app.register_blueprint(compras.bp)
    app.register_blueprint(cajas.bp)
    app.register_blueprint(pedidos.bp)
    app.register_blueprint(ubicaciones.bp)

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))
    
    
    # Migra todos los modelos a la base de datos si falta migrar
    with app.app_context():
        db.create_all()
    
    return app