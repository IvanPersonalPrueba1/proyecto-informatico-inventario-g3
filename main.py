from flask import Flask
from api.routes.user import user_routes
from api.routes.stock import stock_routes  

app = Flask(__name__)

# Registrar las rutas sin prefijos
app.register_blueprint(stock_routes)
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run(debug=True)
