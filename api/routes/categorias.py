from flask import Blueprint, request, jsonify
from api.models.categorias import Category
from api.db.db_config import DBError

category_routes = Blueprint('category_routes', __name__)

# Ruta para obtener todas las categorías
@category_routes.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = Category.get_categories()
        return jsonify({"data": categories}), 200
    except DBError as e:
        return jsonify({"error": str(e)}), 404

# Ruta para crear una nueva categoría
@category_routes.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()

    if not Category.validate(data):
        return jsonify({"error": "Datos inválidos"}), 400

    new_category = Category(data)
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO categories (name) VALUES (%s)', 
        (new_category._name,)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Categoría creada exitosamente"}), 201
