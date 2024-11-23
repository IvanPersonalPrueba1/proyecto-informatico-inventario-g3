from flask import request, jsonify
from api.models.proveedor import Proveedor
from api.utils.security import token_required
from api.db.db_config import DBError
from api import app

@app.route('/user/<int:id_user>/proveedores', methods=['POST'])
@token_required
def create_proveedor(id_user):
    data = request.get_json()
    try:
        proveedor = Proveedor.create_proveedor(id_user, data)
        return jsonify(proveedor), 200
    except Exception as e:
        return jsonify({"message": e.args[0]}), 400


@app.route('/user/<int:id_user>/proveedores/<int:id_proveedor>/productos/<int:id_producto>', methods=['POST'])
@token_required
def add_producto_to_proveedor(id_user, id_proveedor, id_producto):
    try:
        Proveedor.add_producto_to_proveedor(id_user, id_proveedor, id_producto)
        return jsonify({"message": "Producto asociado al proveedor correctamente"}), 200
    except Exception as e:
        return jsonify({"message": e.args[0]}), 400
    
@app.route('/user/<int:id_user>/productos/<int:id_producto>/proveedores', methods=['GET'])
@token_required
def get_proveedores_by_producto(id_user, id_producto):
    try:
        proveedores = Proveedor.get_proveedores_by_producto(id_user, id_producto)
        return jsonify(proveedores), 200
    except Exception as e:
        return jsonify({"message": e.args[0]}), 400


