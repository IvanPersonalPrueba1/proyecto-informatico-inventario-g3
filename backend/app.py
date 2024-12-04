from flask import Flask
from backend.db_connection import create_connection
from backend.routes.user_routes import user_routes

# Crear la instancia de la aplicación Flask
app = Flask(__name__)

# Ruta para probar la conexión a la base de datos
@app.route('/')
def index():
    connection = create_connection()
    
    if connection is not None and connection.is_connected():
        connection.close()
        return "Conexión exitosa a la base de datos MySQL!"
    else:
        return "Error al conectar con la base de datos."

# Registrar las rutas de usuario
app.register_blueprint(user_routes)

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
