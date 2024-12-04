import mysql.connector
from mysql.connector import Error

class User:
    def __init__(self, user_id=None, username=None, email=None, password=None):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password

    def save(self):
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Ajusta si tienes contraseña
                database="mydatabase"
            )
            cursor = connection.cursor()
            query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            values = (self.username, self.email, self.password)
            cursor.execute(query, values)
            connection.commit()
            print(f"User {self.username} added successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

    @staticmethod
    def get_all_users():
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",  # Ajusta si tienes contraseña
                database="mydatabase"
            )
            cursor = connection.cursor(dictionary=True)  # Devuelve resultados como diccionarios
            cursor.execute("SELECT id AS user_id, username, email FROM users")  # Selecciona solo columnas relevantes
            users = cursor.fetchall()
            return users
        except Error as e:
            print(f"Error: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()




