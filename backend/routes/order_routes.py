from flask import Blueprint, jsonify, request
from backend.models.order_model import Order
from backend.models.stock_model import Stock
from backend.models.database import db  # Importamos db para manejar la sesión de SQLAlchemy

# Crear el Blueprint para las rutas de órdenes
order_routes = Blueprint('order_routes', __name__)

# Ruta para obtener todas las órdenes
@order_routes.route('/', methods=['GET'])
def get_orders():
    try:
        orders = Order.query.all()  # Usamos SQLAlchemy para obtener todas las órdenes
        result = []
        for order in orders:
            result.append({
                'order_id': order.order_id,
                'user_id': order.user_id,
                'total': str(order.total),
                'status': order.status,
                'created_at': order.created_at,
            })
        return jsonify({"orders": result}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# Ruta para crear una nueva orden
@order_routes.route('/', methods=['POST'])
def create_order():
    try:
        data = request.get_json()

        if not data or 'user_id' not in data or 'total' not in data or 'status' not in data or 'product_id' not in data or 'quantity' not in data:
            return jsonify({"message": "Bad request, missing required fields."}), 400

        user_id = data['user_id']
        total = data['total']
        status = data['status']
        product_id = data['product_id']
        quantity = data['quantity']

        # Verificamos si el stock es suficiente
        stock = Stock.query.filter_by(product_id=product_id).first()
        if not stock or stock.quantity < quantity:
            return jsonify({"message": "Not enough stock available."}), 400

        # Creamos la nueva orden
        new_order = Order(
            user_id=user_id,
            total=total,
            status=status
        )

        # Añadimos la nueva orden a la base de datos
        db.session.add(new_order)
        db.session.commit()

        # Reducimos el stock disponible
        stock.quantity -= quantity
        db.session.commit()

        # Si es necesario, podrías registrar qué productos fueron ordenados con una tabla intermedia.
        # Si no es así, la orden ya está creada.

        return jsonify({"message": "Order created successfully."}), 201

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# Ruta para actualizar el estado de una orden
@order_routes.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    try:
        data = request.get_json()

        if not data or 'status' not in data:
            return jsonify({"message": "Bad request, missing required fields."}), 400

        status = data['status']

        order = Order.query.get(order_id)  # Buscamos la orden por ID

        if not order:
            return jsonify({"message": "Order not found."}), 404

        order.status = status
        db.session.commit()

        return jsonify({"message": "Order updated successfully."}), 200

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# Ruta para eliminar una orden
@order_routes.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        order = Order.query.get(order_id)

        if not order:
            return jsonify({"message": "Order not found."}), 404

        db.session.delete(order)
        db.session.commit()

        return jsonify({"message": "Order deleted successfully."}), 200

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
