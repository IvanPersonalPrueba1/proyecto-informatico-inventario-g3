from api.db.db_config import get_db_connection, DBError
from flask import request, jsonify
from api import app
import datetime

class Order:
    # Esquema de validación para los datos de la orden
    schema = {
        "products": list
    }

    @classmethod
    def validate(cls, data):
        """ 
        Valida los datos de la orden contra el esquema definido. 

        Verifica que todos los campos están presentes y tienen el tipo correcto.

        Parámetros:
        - data: Diccionario con los datos a validar.

        Retorna:
        - True si los datos son válidos, False en caso contrario.
        """
        if data is None or not isinstance(data, dict):
            return False
        # Control: data contiene todas las claves?
        for key in cls.schema:
            if key not in data:
                return False
            if not isinstance(data[key], cls.schema[key]):
                return False
        return True

    # Constructor base
    def __init__(self, data):
        """ 
        Inicializa un objeto Order con los datos proporcionados. 

        Parámetros:
        - data: Diccionario con los datos de la orden en el siguiente orden:
                (id, order_date, received_date, status, products)
        """
        self.id = data.get("id")
        self.received_date = None  # Inicializar como nula
        self.status = 'pending'  # Estado por defecto
        self.products = data["products"]

    # Conversión a objeto JSON
    def to_json(self):
        """ 
        Convierte el objeto Order a un diccionario JSON. 

        Retorna:
        - Diccionario con los datos de la orden en formato JSON.
        """
        return {
            "id": self.id,
            "received_date": self.received_date,
            "status": self.status,
            "products": self.products
        }

    @classmethod
    def get_orders_by_user(cls, user_id):
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM purchase_orders WHERE user_id = %s', (user_id,))
                orders = cursor.fetchall()
                result = []
                for order in orders:
                    cursor.execute('SELECT * FROM order_products WHERE order_id = %s', (order[0],))
                    products = cursor.fetchall()
                    result.append({
                        "id": order[0],
                        "order_date": order[1],
                        "received_date": order[2],
                        "status": order[3],
                        "products": [
                            {
                                "product_id": product[2],
                                "quantity": product[3]
                            } for product in products
                        ]
                    })
        return result

    @classmethod
    def create_order(cls, user_id, data):
        products = data.get("products")

        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    # Crear la orden en purchase_orders
                    cursor.execute(
                        'INSERT INTO purchase_orders (user_id) VALUES (%s)',
                        (user_id,)
                    )
                    order_id = cursor.lastrowid  # Obtener el order_id generado
                    
                    # Insertar los productos de la orden
                    for product in products:
                        cursor.execute(
                            'INSERT INTO order_products (order_id, product_id, quantity) VALUES (%s, %s, %s)',
                            (order_id, product["product_id"], product["quantity"])
                        )
                    connection.commit()

                except Exception as e:
                    connection.rollback()
                    raise DBError(f"Error al crear la orden: {e}")

        return {"message": "Orden creada exitosamente"}, 200

    @classmethod
    def update_order(cls, user_id, order_id, received_date=None):  # Agregamos received_date como parámetro opcional
        new_status = 'completed'
        received_date = received_date or datetime.date.today()  # Asignar fecha actual si no se proporciona

        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    # Verificar el estado actual de la orden
                    cursor.execute('SELECT status FROM purchase_orders WHERE id = %s AND user_id = %s', (order_id, user_id))
                    current_status = cursor.fetchone()
                    if not current_status:
                        raise DBError("La orden no existe para este usuario.")
                    if current_status[0] != 'pending':
                        raise DBError("Solo se pueden completar órdenes que están en estado 'pendiente'.")

                    # Obtener los productos de la orden y sus cantidades
                    cursor.execute(
                        'SELECT product_id, quantity FROM order_products WHERE order_id = %s',
                        (order_id,)
                    )
                    products = cursor.fetchall()
                    if not products:
                        raise DBError("No se encontraron productos para esta orden.")

                    # Actualizar el stock para cada producto
                    for product_id, quantity in products:
                        cursor.execute(
                            'SELECT quantity FROM stock WHERE product_id = %s AND user_id = %s',
                            (product_id, user_id)
                        )
                        current_stock = cursor.fetchone()
                        if not current_stock:
                            raise DBError(f"El producto {product_id} no tiene stock asociado.")

                        new_quantity = current_stock[0] + quantity
                        cursor.execute(
                            'UPDATE stock SET quantity = %s WHERE product_id = %s AND user_id = %s',
                            (new_quantity, product_id, user_id)
                        )

                    # Actualizar el estado de la orden a 'completed' y establecer la fecha de recepción
                    cursor.execute(
                        'UPDATE purchase_orders SET status = %s, received_date = %s WHERE id = %s AND user_id = %s',
                        (new_status, received_date, order_id, user_id)
                    )

                    connection.commit()

                except Exception as e:
                    connection.rollback()
                    raise DBError(f"Error al actualizar la orden: {e}")

        return {"message": "Orden actualizada y stock modificado exitosamente"}, 200
        

    @classmethod
    def delete_order(cls, user_id, order_id):
        new_status = 'deleted'
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    # Verificar si la orden existe y está en estado 'pending'
                    cursor.execute(
                        'SELECT status FROM purchase_orders WHERE id = %s AND user_id = %s',
                        (order_id, user_id)
                    )
                    order_status = cursor.fetchone()

                    if not order_status:
                        raise DBError("La orden no existe para este usuario.")

                    if order_status[0] != 'pending':
                        raise DBError("Solo se pueden eliminar las órdenes en estado pendiente.")

                    # Cambiar el estado de la orden a 'deleted'
                    cursor.execute(
                        'UPDATE purchase_orders SET status = %s WHERE id = %s AND user_id = %s',
                        (new_status, order_id, user_id)
                    )
                    connection.commit()

                except Exception as e:
                    connection.rollback()
                    raise DBError(f"Error al intentar eliminar la orden: {e}")

        return {"message": "Orden eliminada exitosamente"}, 200

    @classmethod
    def get_order_by_id(cls, user_id, order_id):
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT * FROM purchase_orders WHERE id = %s AND user_id = %s', (order_id, user_id))
                order = cursor.fetchone()
                if not order:
                    raise DBError("No existe la orden solicitada para este usuario.")

                cursor.execute('SELECT * FROM order_products WHERE order_id = %s', (order_id,))
                products = cursor.fetchall()

        return {
            "id": order[0],
            "order_date": order[1],
            "received_date": order[2],
            "status": order[3],
            "products": [
                {
                    "product_id": product[2],
                    "quantity": product[3]
                } for product in products
            ]
        }
