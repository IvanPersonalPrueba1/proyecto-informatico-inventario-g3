from api import app
from flask import request, jsonify
from api.models.categorias import Category
from api.db.db_config import get_db_connection,DBError
from api.utils.security import token_required


@app.route('/user/<int:user_id>/categories', methods=['GET'])
@token_required
def get_categories(user_id):
    try:
        categories = Category.get_categories(user_id)
        if not categories:
            return jsonify({"data": []}), 200 
        return jsonify({"data": categories}), 200
    except DBError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/user/<int:user_id>/categories', methods=['POST'])
@token_required
def create_category(user_id):
    data = request.get_json()

    if not Category.validate(data):
        return jsonify({"error": "Datos inválidos"}), 400

    name = data.get("name")
    descripcion = data.get("descripcion")  
    
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute('SELECT id FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"error": "El usuario no existe"}), 400

        cursor.execute('SELECT id FROM categories WHERE name = %s AND user_id = %s', (name, user_id))
        existing_category = cursor.fetchone()
        if existing_category:
            return jsonify({"error": "Ya existe una categoría con ese nombre para este usuario"}), 400

        cursor.execute('INSERT INTO categories (name, descripcion, user_id) VALUES (%s, %s, %s)', 
                       (name, descripcion, user_id))
        connection.commit()

    except Exception as e:
        return jsonify({"error": f"Error al crear la categoría: {str(e)}"}), 500
    
    finally:
        cursor.close()
        connection.close()

    return jsonify({"message": "Categoría creada exitosamente"}), 201


