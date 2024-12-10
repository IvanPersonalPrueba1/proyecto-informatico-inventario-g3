from api.db.db_config import get_db_connection, DBError

class Order():
    schema = {
        "supplier_id": int,
        "order_date": str,  # Fecha en formato 'YYYY-MM-DD'
        "total_amount": (float, int)
    }

    @staticmethod
    def validate(data):
        supplier_id = data.get("supplier_id")
        order_date = data.get("order_date")
        total_amount = data.get("total_amount")

        if not supplier_id or not isinstance(supplier_id, int):
            return False
        if not order_date or not isinstance(order_date, str):
            return False
        if not total_amount or not isinstance(total_amount, (float, int)) or total_amount < 0:
            return False
        return True

    def __init__(self, data):
        try:
            self._supplier_id = data["supplier_id"]
            self._order_date = data["order_date"]
            self._total_amount = data["total_amount"]
        except KeyError as e:
            raise ValueError(f"Falta la clave esperada: {e}")

    def to_json(self):
        return {
            "supplier_id": self._supplier_id,
            "order_date": self._order_date,
            "total_amount": self._total_amount
        }

    @classmethod
    def get_orders_by_user(cls, user_id):
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT id, supplier_id, order_date, total_amount FROM orders WHERE user_id = %s', (user_id,)
                )
                data = cursor.fetchall()

        if not data:
            raise DBError("No existen órdenes para este usuario.")

        return [
            {
                "id": row[0],
                "supplier_id": row[1],
                "order_date": row[2],
                "total_amount": row[3]
            }
            for row in data
        ]

    @classmethod
    def create_order(cls, user_id, data):
        supplier_id = data.get("supplier_id")
        order_date = data.get("order_date")
        total_amount = data.get("total_amount")

        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    # Verificar si el proveedor existe
                    cursor.execute(
                        'SELECT id FROM suppliers WHERE id = %s AND user_id = %s', (supplier_id, user_id)
                    )
                    supplier_exists = cursor.fetchone()
                    if not supplier_exists:
                        raise DBError("El proveedor especificado no existe para este usuario.")

                    # Crear la orden
                    cursor.execute(
                        'INSERT INTO orders (supplier_id, order_date, total_amount, user_id) VALUES (%s, %s, %s, %s)',
                        (supplier_id, order_date, total_amount, user_id)
                    )
                    connection.commit()

                except DBError as e:
                    raise DBError(f"Error al crear la orden: {str(e)}")
                except Exception as e:
                    raise DBError(f"Error interno del servidor: {str(e)}")

        return {"message": "Orden creada exitosamente"}, 201

    @classmethod
    def update_order(cls, user_id, order_id, data):
        supplier_id = data.get("supplier_id")
        order_date = data.get("order_date")
        total_amount = data.get("total_amount")

        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    # Verificar si el proveedor existe
                    if supplier_id is not None:
                        cursor.execute(
                            'SELECT id FROM suppliers WHERE id = %s AND user_id = %s', (supplier_id, user_id)
                        )
                        supplier_exists = cursor.fetchone()
                        if not supplier_exists:
                            raise DBError("El proveedor especificado no existe para este usuario.")

                    # Actualizar la orden
                    cursor.execute(
                        'UPDATE orders SET supplier_id = %s, order_date = %s, total_amount = %s WHERE id = %s AND user_id = %s',
                        (supplier_id, order_date, total_amount, order_id, user_id)
                    )
                    connection.commit()

                except DBError as e:
                    raise DBError(f"Error al actualizar la orden: {str(e)}")

        return {"message": "Orden actualizada exitosamente"}, 200

    @classmethod
    def delete_order(cls, user_id, order_id):
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    # Verificar si la orden existe
                    cursor.execute(
                        'SELECT id FROM orders WHERE id = %s AND user_id = %s', (order_id, user_id)
                    )
                    existing_order = cursor.fetchone()
                    if not existing_order:
                        raise DBError("La orden no existe para este usuario.")

                    # Eliminar la orden
                    cursor.execute(
                        'DELETE FROM orders WHERE id = %s AND user_id = %s', (order_id, user_id)
                    )
                    connection.commit()

                except DBError as e:
                    raise DBError(f"Error al eliminar la orden: {str(e)}")

        return {"message": "Orden eliminada exitosamente"}, 200

    @classmethod
    def get_order_by_id(cls, user_id, order_id):
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    'SELECT id, supplier_id, order_date, total_amount FROM orders WHERE id = %s AND user_id = %s',
                    (order_id, user_id)
                )
                data = cursor.fetchone()

        if not data:
            raise DBError("No existe la orden solicitada para este usuario.")

        return {
            "id": data[0],
            "supplier_id": data[1],
            "order_date": data[2],
            "total_amount": data[3]
        }

