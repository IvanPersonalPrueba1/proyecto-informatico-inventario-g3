from flask import Blueprint, request, jsonify
from backend.models.user_model import User

user_routes = Blueprint('user_routes', __name__)

# Ruta para agregar un nuevo usuario
@user_routes.route('/user', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        if 'username' not in data or 'email' not in data or 'password' not in data:
            return jsonify({"message": "Bad request, missing required fields."}), 400

        username = data['username']
        email = data['email']
        password = data['password']

        new_user = User(username=username, email=email, password=password)
        new_user.save()

        return jsonify({"message": "User added successfully."}), 201
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# Ruta para obtener todos los usuarios
@user_routes.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.get_all_users()
        if not users:
            return jsonify({"users": []}), 200
        return jsonify({"users": users}), 200
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500


