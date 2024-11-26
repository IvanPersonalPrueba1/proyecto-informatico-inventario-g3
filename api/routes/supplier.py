from flask import request, jsonify
from api.models.supplier import Supplier
from api.utils.security import token_required
from api.db.db_config import DBError
from api import app

@app.route('/user/<int:user_id>/supplier', methods=['POST'])
@token_required
def create_supplier(user_id):
    data = request.get_json()
    try:
        supplier = Supplier.create_supplier(user_id, data)
        return jsonify(supplier), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400


@app.route('/user/<int:user_id>/suppliers/<int:supplier_id>/products/<int:product_id>', methods=['POST'])
@token_required
def add_product_to_supplier(user_id, supplier_id, product_id):
    try:
        Supplier.add_product_to_supplier(user_id=user_id, supplier_id=supplier_id, product_id=product_id)
        return jsonify({"message": "Producto asociado al proveedor correctamente"}), 200
    except Exception as e:
        print(f"Error encontrado: {e}")
        return jsonify({"message": e.args[0]}), 400


    
@app.route('/user/<int:user_id>/products/<int:product_id>/supplier', methods=['GET'])
@token_required
def get_proveedores_by_producto(user_id, product_id):
    try:
        suppliers= Supplier.get_proveedores_by_producto(user_id, product_id)
        return jsonify(suppliers), 200
    except Exception as e:
        return jsonify({"message": e.args[0]}), 400


@app.route('/user/<int:user_id>/suppliers', methods=['GET'])
@token_required
def get_suppliers_by_user(user_id):
    """
    Devuelve todos los proveedores asociados a un usuario.
    """
    try:
        suppliers = Supplier.get_suppliers_by_user(user_id)
        return jsonify(suppliers), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 400