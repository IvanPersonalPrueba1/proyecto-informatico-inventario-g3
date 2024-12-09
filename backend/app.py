# app.py
from flask import Flask, request, jsonify
from api.db.db_connector import get_db_connection
from api.db.models.user import User
from api.db.models.stock import Stock
from api.db.models.supplier import Supplier

app = Flask(__name__)

# Rutas de Usuarios
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    connection = get_db_connection()  # Conexión creada dentro de la función
    response, status_code = User.register(data)  # Llamada a User.register sin el argumento connection
    connection.close()
    return jsonify(response), status_code

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth:
        return jsonify({"message": "No se proporcionó autorización"}), 401

    response, status_code = User.login(auth)  # Solo pasa `auth`, no `connection`
    return jsonify(response), status_code

# Rutas de Productos (Stock)
@app.route('/products', methods=['GET'])
def list_products():
    connection = get_db_connection()
    products, status_code = Stock.list_all(connection)
    connection.close()
    return jsonify(products), status_code

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()

    # Verificar si los datos contienen los campos necesarios
    if not all(key in data for key in ["product_id", "quantity", "supplier_id"]):
        return jsonify({"message": "Faltan datos: product_id, quantity, supplier_id"}), 400

    connection = get_db_connection()
    response, status_code = Stock.add(data, connection)
    connection.close()
    return jsonify(response), status_code

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.get_json()
    connection = get_db_connection()
    response, status_code = Stock.update(product_id, data, connection)
    connection.close()
    return jsonify(response), status_code

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    connection = get_db_connection()
    response, status_code = Stock.delete(product_id, connection)
    connection.close()
    return jsonify(response), status_code

# Rutas de Proveedores (Suppliers)
@app.route('/suppliers', methods=['GET'])
def list_suppliers():
    connection = get_db_connection()
    suppliers, status_code = Supplier.list_all(connection)
    connection.close()
    return jsonify(suppliers), status_code

@app.route('/suppliers', methods=['POST'])
def add_supplier():
    data = request.get_json()
    connection = get_db_connection()
    response, status_code = Supplier.add(data, connection)
    connection.close()
    return jsonify(response), status_code

@app.route('/suppliers/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    data = request.get_json()
    connection = get_db_connection()
    response, status_code = Supplier.update(supplier_id, data, connection)
    connection.close()
    return jsonify(response), status_code

@app.route('/suppliers/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    connection = get_db_connection()
    response, status_code = Supplier.delete(supplier_id, connection)
    connection.close()
    return jsonify(response), status_code

if __name__ == '__main__':
    app.run(debug=True)
