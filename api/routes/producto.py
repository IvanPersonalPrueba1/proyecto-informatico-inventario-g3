from api import app
from api.models.producto import Product
from flask import jsonify, request
from api.utils.security import token_required
from api.db.db_config import get_db_connection, DBError

@app.route('/user/<int:usuario_id>/products', methods=['GET'])
@token_required
def get_products(usuario_id):
    try:
        products = Product.get_products_by_user(usuario_id)
        return jsonify({"data": products}), 200
    except DBError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/user/<int:usuario_id>/products', methods=['POST'])
@token_required
def create_product(usuario_id):
    data = request.get_json()
    
    if not Product.validate(data):
        return jsonify({"error": "Datos inválidos"}), 400
    
    new_product = Product(data)
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO productos (nombre, precio, usuario_id, categoria_id) VALUES (%s, %s, %s, %s)', 
            (new_product.name, new_product.price, usuario_id, new_product.category_id)
        )
        connection.commit()
    except Exception as e:
        return jsonify({"error": f"Error al crear el producto: {str(e)}"}), 500
    finally:
        cursor.close()
        connection.close()
    return jsonify({"message": "Producto creado exitosamente"}), 201
