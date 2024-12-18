from api import app
from flask import jsonify, request
from api.models.reports import Report
from api.utils.security import token_required
from api.db.db_config import DBError

@app.route('/user/<int:user_id>/reports/summary', methods=['GET'])
@token_required
def report_purchases_summary(user_id):
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not start_date or not end_date:
        return jsonify({"error": "Se requieren las fechas 'start_date' y 'end_date'"}), 400

    try:
        data = Report.purchases_summary_by_period(user_id, start_date, end_date)
        return jsonify({"data": data}), 200
    except DBError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/user/<int:user_id>/reports/top-suppliers', methods=['GET'])
@token_required
def report_top_suppliers(user_id):
    limit = request.args.get('limit', 5, type=int)

    try:
        data = Report.top_suppliers(user_id, limit)
        return jsonify({"data": data}), 200
    except DBError as e:
        return jsonify({"error": str(e)}), 404

@app.route('/user/<int:user_id>/reports/top-products', methods=['GET'])
@token_required
def report_top_products(user_id):
    limit = request.args.get('limit', 5, type=int)

    try:
        data = Report.top_products(user_id, limit)
        return jsonify({"data": data}), 200
    except DBError as e:
        return jsonify({"error": str(e)}), 404