from flask import Blueprint, request, jsonify
from backend.models.user_model import User
from backend.models.order_model import Order
import mysql.connector

user_routes = Blueprint('user_routes', __name__)

# Ruta para generar reportes
@user_routes.route('/report/orders', methods=['GET'])
def get_orders_report():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Cambia si tu usuario es diferente
            password="",  # Cambia si tienes contraseña
            database="mydatabase"
        )
        cursor = connection.cursor()

        # Consulta para obtener el reporte consolidado
        query = """
            SELECT 
                o.id AS order_id,
                o.total AS order_total,
                u.username AS user_name,
                u.email AS user_email
            FROM orders o
            JOIN users u ON o.user_id = u.id;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # Procesar los datos del reporte
        report = []
        for row in results:
            report.append({
                "order_id": row[0],
                "order_total": row[1],
                "user_name": row[2],
                "user_email": row[3]
            })

        return jsonify({"report": report}), 200

    except mysql.connector.Error as e:
        return jsonify({"message": f"Database error: {e}"}), 500

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()




