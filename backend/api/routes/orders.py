from api import app
from flask import request, jsonify
from api.models.orders import Order
from api.db.db_config import DBError
from api.utils.security import token_required

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
    Actualiza una orden existente.

    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: ID del usuario que creó la orden.
      - name: order_id
        in: path
        type: integer
        required: true
        description: ID de la orden a actualizar.
      - name: received_date
        in: body
        type: string
        required: true
        description: Fecha de recepción de la orden (YYYY-MM-DD).
    responses:
      200:
        description: Orden actualizada exitosamente.
      400:
        description: Datos inválidos o error al actualizar la orden.
      404:
        description: Orden no encontrada para este usuario.
      500:
        description: Error interno del servidor.
    """
    data = request.get_json()
    received_date = data.get("received_date")

    if not received_date or not isinstance(received_date, str):
        return jsonify({"error": "Fecha de recepción inválida"}), 400

    try:
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
