from api import app
from api.models.producto import Product
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
    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM products WHERE user_id = %s AND name = %s', (user_id, data["name"]))
    existing_product = cursor.fetchall()

    if existing_product:
        cursor.close()
        connection.close()
        return jsonify({"error": "El producto ya existe para este usuario"}), 400
    
    try:
        new_product = Product(data)  
    except KeyError as e:
        return jsonify({"error": f"Falta una clave en los datos: {e}"}), 400
        
    try:
        cursor.execute(
            'INSERT INTO products (name, price, category_id, user_id) VALUES (%s, %s, %s, %s)', 
            (new_product._name, new_product._price, new_product._category_id, user_id)
        )
        connection.commit()
    except Exception as e:
        return jsonify({"error": f"Error al crear el producto: {str(e)}"}), 500
    finally:
        cursor.close()
        connection.close()
        
    return jsonify({"message": "Producto creado exitosamente"}), 201
