from flask import Flask
from api.routes. producto import product_routes
from api.routes.categorias import category_routes
from api.routes.user import user_routes

app = Flask(__name__)

# Registrar las rutas
app.register_blueprint(product_routes)
app.register_blueprint(category_routes)
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(debug=True)
