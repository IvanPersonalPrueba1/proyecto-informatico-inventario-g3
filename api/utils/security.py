from flask import request, jsonify
import jwt
from functools import wraps
from api import app
from api.db.db_config import get_db_connection, DBError

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token', None)
        if not token:
            return jsonify({"message": "Token faltante"}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            request.user_id = data.get('id')  
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expirado"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Token inválido"}), 401

        return func(*args, **kwargs)
    return decorated