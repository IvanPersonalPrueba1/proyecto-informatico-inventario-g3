from api import app
from flask import jsonify, request
from api.models.stock import Stock
from api.db.db_config import DBError
from api.utils.security import token_required

# Ruta para actualizar el stock de un producto
@app.route('/user/<int:id_user>/stock/<int:producto_id>', methods=['PUT'])
@token_required
def update_stock(id_user, producto_id):
    try:
        data = request.get_json()
        
        # Validar la entrada
        if not Stock.validate(data):
            return jsonify({"error": "Datos inválidos"}), 400
        
        # Actualizar el stock asociado al usuario
        new_quantity = data["quantity"]
        result = Stock.update_stock(id_user, producto_id, new_quantity)
        
        return jsonify(result), 200
    except DBError as e:
        return jsonify({"error": str(e)}), 400


# Ruta para verificar productos con bajo stock
@app.route('/user/<int:id_user>/stock/low', methods=['GET'])
@token_required
def check_low_stock(id_user):
    try:
        # Obtener el umbral opcional desde los parámetros de la URL
        threshold = request.args.get('threshold', default=10, type=int)
        
        # Consultar productos con bajo stock para el usuario
        low_stock_products = Stock.check_low_stock(id_user, threshold)
        
        return jsonify({"data": low_stock_products}), 200
    except DBError as e:
        return jsonify({"error": str(e)}), 400


# Ruta para obtener todos los productos en stock según usuario
@app.route('/user/<int:id_user>/stock', methods=['GET'])
@token_required
def get_stock_by_user(id_user):
    try:
        stock = Stock.get_stock_by_user(id_user)
        return jsonify(stock), 200
    except Exception as e:
        return jsonify({"message": e.args[0]}), 400
