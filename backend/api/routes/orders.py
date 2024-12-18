from api import app
from flask import request, jsonify
from api.models.orders import Order
from api.db.db_config import DBError
from api.utils.security import token_required
import datetime


@app.route('/user/<int:user_id>/orders', methods=['GET'])
@token_required
def get_orders(user_id):
    try:
        orders = Order.get_orders_by_user(user_id)
        return jsonify({"data": orders}), 200
    except DBError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/user/<int:user_id>/orders', methods=['POST'])
@token_required
def create_order(user_id):
    data = request.get_json()

    if not Order.validate(data):
        return jsonify({"error": "Datos inválidos"}), 400

    try:
        message, status_code = Order.create_order(user_id, data)
        return jsonify(message), status_code
    except DBError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500



@app.route('/user/<int:user_id>/orders/<int:order_id>', methods=['PUT'])
@token_required
def update_order(user_id, order_id):
    """
    Confirma una orden de compra, actualizando su estado a 'completado' y asignando la fecha de recepción.
    """
    received_date = None  # Inicializar como None por defecto

    data = request.get_data()  # Obtener cuerpo de la solicitud
    if data:  # Si se recibe un cuerpo, procesarlo
        try:
            data = request.get_json()
            received_date = data.get("received_date")

            # Validar el formato de la fecha en caso de que se reciba
            if received_date:
                try:
                    datetime.datetime.strptime(received_date, '%Y-%m-%d')  # Validar formato
                except ValueError:
                    return jsonify({"error": "Formato de fecha inválido. Usa YYYY-MM-DD."}), 400
        except Exception as e:
            return jsonify({"error": "Error al decodificar el JSON."}), 400

    try:
        # Llamar al modelo con received_date (puede ser None o la fecha proporcionada)
        message, status_code = Order.update_order(user_id, order_id, received_date)
        return jsonify(message), status_code
    except DBError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/user/<int:user_id>/orders/<int:order_id>', methods=['DELETE'])
@token_required
def delete_order(user_id, order_id):
    try:
        message, status_code = Order.delete_order(user_id, order_id)
        return jsonify(message), status_code
    except DBError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/user/<int:user_id>/orders/<int:order_id>', methods=['GET'])
@token_required
def get_order_by_id(user_id, order_id):
    try:
        order = Order.get_order_by_id(user_id, order_id)
        return jsonify(order), 200
    except DBError as e:
        return jsonify({"error": str(e)}), 400
