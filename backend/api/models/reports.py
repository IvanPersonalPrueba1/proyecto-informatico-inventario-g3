from api.db.db_config import get_db_connection, DBError

class Report:
    @staticmethod
    def purchases_summary_by_period(user_id, start_date, end_date):
        """
        Genera un resumen de compras realizadas por un usuario en un periodo específico.
        """
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT o.order_date, s.name_supplier AS supplier_name, 
                           SUM(op.quantity * p.price) AS total_amount
                    FROM purchase_orders o
                    JOIN order_products op ON o.id = op.order_id
                    JOIN products p ON op.product_id = p.id
                    JOIN suppliers s ON o.supplier_id = s.id
                    WHERE o.user_id = %s AND o.order_date BETWEEN %s AND %s
                    GROUP BY o.id, s.name_supplier
                    ORDER BY o.order_date ASC
                    ''',
                    (user_id, start_date, end_date)
                )
                data = cursor.fetchall()

        if not data:
            raise DBError("No se encontraron compras en el período especificado.")

        return [
            {"order_date": row[0], "supplier_name": row[1], "total_amount": row[2]}
            for row in data
        ]

    @staticmethod
    def top_suppliers(user_id, limit=5):
        """
        Obtiene los proveedores con mayor número de órdenes realizadas por el usuario.
        """
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT s.name_supplier AS supplier_name, COUNT(o.id) AS total_orders
                    FROM purchase_orders o
                    JOIN suppliers s ON o.supplier_id = s.id
                    WHERE o.user_id = %s
                    GROUP BY s.id
                    ORDER BY total_orders DESC
                    LIMIT %s
                    ''',
                    (user_id, limit)
                )
                data = cursor.fetchall()

        if not data:
            raise DBError("No se encontraron proveedores con órdenes registradas.")

        return [
            {"supplier_name": row[0], "total_orders": row[1]}
            for row in data
        ]

    @staticmethod
    def top_products(user_id, limit=5):
        """
        Obtiene los productos más comprados por el usuario.
        """
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT p.name AS product_name, SUM(op.quantity) AS total_quantity
                    FROM order_products op
                    JOIN products p ON op.product_id = p.id
                    JOIN purchase_orders o ON op.order_id = o.id
                    WHERE o.user_id = %s
                    GROUP BY p.id
                    ORDER BY total_quantity DESC
                    LIMIT %s
                    ''',
                    (user_id, limit)
                )
                data = cursor.fetchall()

        if not data:
            raise DBError("No se encontraron productos comprados.")

        return [
            {"product_name": row[0], "total_quantity": row[1]}
            for row in data
        ]

    @staticmethod
    def total_expenses_by_supplier(user_id):
        """
        Obtiene los gastos totales realizados a cada proveedor por el usuario.
        """
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT s.name_supplier AS supplier_name, 
                           SUM(op.quantity * p.price) AS total_spent
                    FROM purchase_orders o
                    JOIN order_products op ON o.id = op.order_id
                    JOIN products p ON op.product_id = p.id
                    JOIN suppliers s ON o.supplier_id = s.id
                    WHERE o.user_id = %s
                    GROUP BY s.id
                    ORDER BY total_spent DESC
                    ''',
                    (user_id,)
                )
                data = cursor.fetchall()

        if not data:
            raise DBError("No se encontraron gastos registrados para los proveedores.")

        return [
            {"supplier_name": row[0], "total_spent": row[1]}
            for row in data
        ]
