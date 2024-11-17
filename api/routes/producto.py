from flask import Blueprint, request, jsonify
from api.models.producto import Product
from api.db.db_config import DBError

product_routes = Blueprint('product_routes', __name__)

# Ruta para obtener todos los productos de un usuario
@product_routes.route('/products/<int:id_user>', methods=['GET'])
def get_products(id_user):
    try:
        products = Product.get_products_by_user(id_user)
        return jsonify({"data": products}), 200
    except DBError as e:
        return jsonify({"error": str(e)}), 404

# Ruta para crear un nuevo producto
@product_routes.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    
    if not Product.validate(data):
        return jsonify({"error": "Datos inválidos"}), 400
    
    # Suponiendo que el usuario está logueado y se obtiene su id
    id_user = 1  # Esto debería cambiar con la lógica de autenticación.
    
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
