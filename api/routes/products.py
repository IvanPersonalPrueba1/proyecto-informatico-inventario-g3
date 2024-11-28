from api import app
from api.models.products import Product
from flask import jsonify, request
from api.utils.security import token_required
from api.db.db_config import get_db_connection, DBError

@app.route('/user/<int:user_id>/products', methods=['GET'])
@token_required
def get_products(user_id):
    try:
        products = Product.get_products_by_user(user_id)
        return jsonify({"data": products}), 200
    except DBError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/user/<int:user_id>/products', methods=['POST'])
@token_required
def create_product(user_id):
    data = request.get_json()
                
    if not Product.validate(data):
        return jsonify({"error": "Datos inválidos"}), 400

    try:
        message, status_code = Product.create_product(user_id, data)
        return jsonify(message), status_code

    except DBError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
    
@app.route('/user/<int:user_id>/products/<int:product_id>', methods=['PUT'])
@token_required
def update_product(user_id, product_id):
    data = request.get_json()

    if not Product.validate(data):
        return jsonify({"error": "Datos inválidos"}), 400

    try:
        message, status_code = Product.update_product(user_id, product_id, data)
        return jsonify(message), status_code
    except DBError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/user/<int:user_id>/products/<int:product_id>', methods=['DELETE'])
@token_required
def delete_product(user_id, product_id):
    try:
        message, status_code = Product.delete_product(user_id, product_id)
        return jsonify(message), status_code
    except DBError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
