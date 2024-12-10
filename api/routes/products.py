from api import app
from flask import request, jsonify
from api.models.products import Product
from api.db.db_config import get_db_connection, DBError
from api.utils.security import token_required

@app.route('/user/<int:user_id>/products', methods=['GET'])
@token_required
def get_products(user_id):
    #Obtener todos los productos de un usuario.
    try:
        products = Product.get_products_by_user(user_id)
        return jsonify({"data": products}), 200
    except DBError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/user/<int:user_id>/products', methods=['POST'])
@token_required
def create_product(user_id):
    #Crear un nuevo producto para un usuario.
    data = request.get_json()
                
    if not Product.validate(data):
        return jsonify({"error": "Datos inválidos"}), 400

    try:
        message, status_code = Product.create_product(user_id, data)
        return jsonify(message), status_code

    except DBError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500
    
@app.route('/user/<int:user_id>/products/<int:product_id>', methods=['PUT'])
@token_required
def update_product(user_id, product_id):
    #Actualizar un producto existente de un usuario.
    data = request.get_json()

    if not Product.validate(data):
        return jsonify({"error": "Datos inválidos"}), 400

    try:
        message, status_code = Product.update_product(user_id, product_id, data)
        return jsonify(message), status_code
    except DBError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/user/<int:user_id>/products/<int:product_id>', methods=['DELETE'])
@token_required
def delete_product(user_id, product_id):
    try:
        message, status_code = Product.delete_product(user_id, product_id)
        return jsonify(message), status_code
    except DBError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error interno del servidor"}), 500

@app.route('/user/<int:user_id>/products/<int:category_id>', methods=['GET'])
@token_required
def get_products_by_category(user_id, category_id):
    if category_id == 0:
        category_id = None

    try:
        products = Product.get_products_by_category_id(user_id, category_id)
        return jsonify(products), 200
    except DBError as e:
        return jsonify({"message": str(e)}), 400
