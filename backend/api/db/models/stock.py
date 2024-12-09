# api/db/models/stock.py
import mysql.connector
from flask import jsonify

class Stock:
    @staticmethod
    def add(data, connection):
        """Agrega un nuevo producto al inventario."""
        # Verificar que los campos necesarios estén en el data
        if not all(key in data for key in ["product_id", "quantity", "supplier_id", "user_id"]):
            return {"message": "Faltan datos: product_id, quantity, supplier_id, user_id"}, 400

        # Si los campos están, proceder con la inserción
        try:
            values = (data["product_id"], data["quantity"], data["supplier_id"], data["user_id"])
            cursor = connection.cursor()
            query = "INSERT INTO stock (product_id, quantity, supplier_id, user_id) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            return {"message": "Producto agregado correctamente."}, 201
        except Exception as e:
            return {"message": str(e)}, 500

    @staticmethod
    def list_all(connection):
        """Lista todos los productos."""
        query = "SELECT * FROM stock"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows, 200

    @staticmethod
    def update(product_id, data, connection):
        """Actualiza un producto."""
        query = "UPDATE stock SET product_id = %s, quantity = %s, supplier_id = %s, user_id = %s WHERE id = %s"
        values = (data["product_id"], data["quantity"], data["supplier_id"], data["user_id"], product_id)
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        return {"message": "Producto actualizado correctamente."}, 200

    @staticmethod
    def delete(product_id, connection):
        """Elimina un producto."""
        query = "DELETE FROM stock WHERE id = %s"
        cursor = connection.cursor()
        cursor.execute(query, (product_id,))
        connection.commit()
        cursor.close()
        return {"message": "Producto eliminado correctamente."}, 200
