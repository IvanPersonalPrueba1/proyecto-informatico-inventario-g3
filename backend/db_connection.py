import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='mydatabase'
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos")
            return connection
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

# Probar la conexión
if __name__ == "__main__":
    connection = create_connection()
    if connection:
        connection.close()
