from flask import Blueprint, jsonify
from backend.models.database import db

report_bp = Blueprint('report_routes', __name__)

# Reporte de productos con bajo stock
@report_bp.route('/api/reports/low-stock', methods=['GET'])
def low_stock_report():
    try:
        query = """
        SELECT product_id, product_name, quantity
        FROM stock
        WHERE quantity < 10
        ORDER BY quantity ASC;
        """
        result = db.session.execute(query).fetchall()
        low_stock_products = [
            {"product_id": row[0], "product_name": row[1], "quantity": row[2]}
            for row in result
        ]
        return jsonify({"low_stock_products": low_stock_products})
    except Exception as e:
        return jsonify({"message": f"Error retrieving low stock products: {str(e)}"}), 500

# Reporte del historial de órdenes
@report_bp.route('/api/reports/order-history', methods=['GET'])
def order_history_report():
    try:
        query = """
        SELECT o.order_id, u.username, o.total, o.status, o.created_at
        FROM orders o
        INNER JOIN users u ON o.user_id = u.id
        ORDER BY o.created_at DESC;
        """
        result = db.session.execute(query).fetchall()
        order_history = [
            {
                "order_id": row[0],
                "username": row[1],
                "total": row[2],
                "status": row[3],
                "created_at": row[4].isoformat()
            }
            for row in result
        ]
        return jsonify({"order_history": order_history})
    except Exception as e:
        return jsonify({"message": f"Error retrieving order history: {str(e)}"}), 500

# Reporte del inventario actual
@report_bp.route('/api/reports/current-inventory', methods=['GET'])
def current_inventory_report():
    try:
        query = """
        SELECT p.id AS product_id, p.name AS product_name, s.quantity AS stock_quantity
        FROM products p
        LEFT JOIN stock s ON p.id = s.product_id
        ORDER BY p.name;
        """
        result = db.session.execute(query).fetchall()
        inventory = [
            {"product_id": row[0], "product_name": row[1], "stock_quantity": row[2]}
            for row in result
        ]
        return jsonify({"current_inventory": inventory})
    except Exception as e:
        return jsonify({"message": f"Error retrieving current inventory: {str(e)}"}), 500

