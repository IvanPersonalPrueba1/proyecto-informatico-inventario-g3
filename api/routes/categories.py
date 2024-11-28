from api import app
from flask import request, jsonify
from api.models.categories import Category
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

    try:
        message, status_code = Category.create_category(user_id, data)
        return jsonify(message), status_code

    except DBError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/user/<int:user_id>/categories/<int:category_id>', methods=['PUT'])
@token_required
def update_category(user_id, category_id):
    data = request.get_json()

    if not Category.validate(data):
        return jsonify({"error": "Datos inválidos"}), 400

    try:
        message, status_code = Category.update_category(user_id, category_id, data)
        return jsonify(message), status_code
    except DBError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500

@app.route('/user/<int:user_id>/categories/<int:category_id>', methods=['DELETE'])
@token_required
def delete_category(user_id, category_id):
    try:
        message, status_code = Category.delete_category(user_id, category_id)
        return jsonify(message), status_code
    except DBError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error"}), 500
