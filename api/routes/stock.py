from flask import Blueprint, request, jsonify
from api.models.stock import Stock
from api.db.db_config import DBError
import logging

stock_routes = Blueprint('stock_routes', __name__)

# Ruta para actualizar el stock de un producto
@stock_routes.route('/stock/<int:producto_id>', methods=['PUT'])
def update_stock(producto_id):
    try:
        data = request.get_json()
        
        # Validar la entrada
        if not Stock.validate(data):
            logging.error(f"Invalid data received: {data}")
            return jsonify({"error": "Datos inválidos"}), 400
        
        # Actualizar el stock
        new_quantity = data["quantity"]
        result = Stock.update_stock(producto_id, new_quantity)
        
        return jsonify(result), 200
    except DBError as e:
        return jsonify({"error": str(e)}), 500

# Ruta para verificar productos con bajo stock
@stock_routes.route('/stock/low', methods=['GET'])
def check_low_stock():
    try:
        # Obtener el umbral opcional desde los parámetros de la URL
        threshold = request.args.get('threshold', default=10, type=int)
        
        # Consultar productos con bajo stock
        low_stock_products = Stock.check_low_stock(threshold)
        
        return jsonify({"data": low_stock_products}), 200
    except DBError as e:
        return jsonify({"error": str(e)}), 500

# Ruta para obtener todos los productos en stock
@stock_routes.route('/stock', methods=['GET'])
def get_all_stock():
    try:
        all_stock = Stock.get_all_stock()
        return jsonify({"data": all_stock}), 200
    except DBError as e:
        return jsonify({"error": str(e)}), 500
