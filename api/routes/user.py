from api import app
from flask import request, jsonify
from api.models.user import User
from api.db.db_config import DBError


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    try:
        response = User.register(data)
        return jsonify(response), 201  
    except Exception as e:
        if isinstance(e, DBError):
            info = e.args[0]
            return jsonify(info), info["code"]
        return jsonify({"message": e.args[0]}), 400
    
@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    try:
        user = User.login(auth)
        return jsonify( user ), 200
    except Exception as e:
        if isinstance(e, DBError):
            info = e.args[0]
            return jsonify(info), info["code"]
        return jsonify( {"message": e.args[0]} ), 400
