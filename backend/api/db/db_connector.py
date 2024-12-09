import mysql.connector

def get_db_connection():
    """Establece la conexión a la base de datos."""
    return mysql.connector.connect(
        host="localhost",  # Cambiar si usas otro host
        user="root",  # Cambia por tu usuario de la base de datos
        password="",  # Cambia por tu contraseña
        database="gestion_stock"  # Cambia por el nombre de tu base de datos
    )
