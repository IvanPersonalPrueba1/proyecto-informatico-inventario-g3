from api import app
from api.models.producto import Product
from flask import jsonify, request
from api.utils.security import token_required
from api.db.db_config import get_db_connection, DBError

# Ruta para obtener todos los productos de un usuario
@app.route('/products', methods=['GET'])
@token_required
def get_products():
    user_id = request.user_id
    try:
        products = Product.get_products_by_user(user_id)
        return jsonify({"data": products}), 200
    except DBError as e:
        return jsonify({"error": str(e)}), 404

# Ruta para crear un nuevo producto
@app.route('/products', methods=['POST'])
@token_required
def create_product():
    data = request.get_json()
    
    if not Product.validate(data):
        return jsonify({"error": "Datos inválidos"}), 400
    
    id_user = getattr(request, "user_id", None)  
    
    if not id_user:
        return jsonify({"error": "Usuario no autenticado"}), 401
    
    new_product = Product(data)
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO products (name, price, id_user) VALUES (%s, %s, %s)', 
        (new_product._name, new_product._price, id_user)
    )
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({"message": "Producto creado exitosamente"}), 201
