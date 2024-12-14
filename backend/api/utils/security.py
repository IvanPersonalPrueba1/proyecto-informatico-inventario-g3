from flask import request, jsonify
import jwt
from functools import wraps
from api import app
from api.db.db_config import get_db_connection, DBError


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        #print(kwargs)
        token = None

        # Verificar si se incluye 'x-access-token' en los headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({"message": "Falta el token"}), 401

        user_id = None
 
        # Verificar si 'id_user' está en los argumentos de la ruta
        # print("Argumentos de la solicitud: ", kwargs)
        if 'user_id' in kwargs:
            user_id = kwargs['user_id']

        if user_id is None:
            # Si no está en la ruta, buscar en los headers
            if 'user_id' in request.headers:
                user_id = request.headers['user_id']

        if user_id is None:
            # Si no se encuentra, denegar el acceso
            return jsonify({"message": "Falta el usuario"}), 401

        try:
            # Decodificar el token y validar que el id_user coincide con el propietario del token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            token_id = data['id']

            if int(user_id) != int(token_id):
                return jsonify({"message": "Error de id"}), 401
        except Exception as e:
            print(e)
            return jsonify({"message": str(e)}), 401

        # Continuar con la ejecución de la función protegida
        return func(*args, **kwargs)
    return decorated

