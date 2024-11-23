from flask import request, jsonify
import jwt
from functools import wraps
from api import app
from api.db.db_config import get_db_connection, DBError


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        print(kwargs)
        token = None

        # Verificar si se incluye 'x-access-token' en los headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({"message": "Falta el token"}), 401

        id_user = None
 
        # Verificar si 'id_user' está en los argumentos de la ruta
        print("Argumentos de la solicitud: ", kwargs)
        if 'id_user' in kwargs:
            id_user = kwargs['id_user']

        if id_user is None:
            # Si no está en la ruta, buscar en los headers
            if 'id_user' in request.headers:
                id_user = request.headers['id_user']

        if id_user is None:
            # Si no se encuentra, denegar el acceso
            return jsonify({"message": "Falta el usuario"}), 401

        try:
            # Decodificar el token y validar que el id_user coincide con el propietario del token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            token_id = data['id']

            if int(id_user) != int(token_id):
                return jsonify({"message": "Error de id"}), 401
        except Exception as e:
            print(e)
            return jsonify({"message": str(e)}), 401

        # Continuar con la ejecución de la función protegida
        return func(*args, **kwargs)
    return decorated
