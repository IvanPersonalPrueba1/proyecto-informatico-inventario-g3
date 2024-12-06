from flask import Flask
from backend.models.database import db
from backend.routes.report_routes import report_bp
from backend.routes.order_routes import order_routes  # Importar las rutas de órdenes

app = Flask(__name__)

# Configurar conexión a la base de datos (ajustado para phpMyAdmin)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Registrar blueprints
app.register_blueprint(report_bp)  # Blueprints para reportes
app.register_blueprint(order_routes, url_prefix='/orders')  # Blueprints para órdenes

if __name__ == '__main__':
    app.run(debug=True)




