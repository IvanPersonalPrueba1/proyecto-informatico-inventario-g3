from api.db.db_config import get_db_connection, DBError
from api import app

class Stock:
    # Solo se valida 'quantity'
    schema = {
        "quantity": int  # La cantidad debe ser un número entero
    }

    @classmethod
    def validate(cls, data):
        """
        Valida que los datos proporcionados contengan solo 'quantity'.

        Parámetros:
        - data: Diccionario con los datos a validar.

        Retorna:
        - True si los datos son válidos, False en caso contrario.
        """

        if data is None or not isinstance(data, dict):
            return False

        # Control: data contiene todas las claves requeridas?
        for key in cls.schema:
            if key not in data:
                return False
            # Control: cada valor es del tipo correcto
            if not isinstance(data[key], cls.schema[key]):
                return False

        return True

    # Constructor base
    def __init__(self, data):
        """
        Inicializa un objeto Stock con los datos proporcionados.

        Parámetros:
        - data: Tupla con los datos del stock (product_id, product_name, quantity).
        """
        
        self.product_id = data[0]
        self.product_name = data[1]
        self.quantity = data[2]

    # Conversión a objeto JSON
    def to_json(self):
        """ 
        Convierte el objeto Stock a un diccionario JSON. 

        Retorna:
        - Diccionario con los dato de stock en formato JSON.
        """
            
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity
        }

    @classmethod
    def update_stock(cls, user_id, product_id, new_quantity):
        """
        Actualiza la cantidad de productos en stock asociados a un usuario específico.

        Parámetros:
        - user_id: ID del usuario autenticado.
        - product_id: ID del producto.
        - new_quantity: Nueva cantidad para el producto.

        Levanta:
        - DBError: Si la nueva cantidad es menor o igual a 0, si el producto no existe o no pertenece al usuario,
        o si hay un error durante la actualización en la base de datos.

        Retorna:
        - Un mensaje indicando el resultado de la actualización del stock.
        """

        if new_quantity <= 0:
            raise DBError("La cantidad debe ser mayor a 0")

        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute(
                'SELECT quantity FROM stock WHERE product_id = %s AND user_id = %s',
                (product_id, user_id)
            )
            current_quantity = cursor.fetchone()
            
            if not current_quantity:
                raise DBError("El producto no existe o no pertenece al usuario")
            
            if current_quantity[0] == new_quantity:
                return {"message": "Stock no actualizado, esa cantidad es igual a la actual"}
            
            cursor.execute(
                'UPDATE stock SET quantity = %s WHERE product_id = %s AND user_id = %s',
                (new_quantity, product_id, user_id)
            )
            
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            connection.rollback()
            cursor.close()
            connection.close()
            raise DBError(f"Error actualizando el stock: {e}")
        
        return {"message": "Stock actualizado exitosamente"}

    @classmethod
    def check_low_stock(cls, user_id, threshold=10):
        """
        Verifica si algún producto asociado al usuario tiene stock bajo.
        Retorna una lista de productos con stock bajo.

        Parámetros:
        - user_id: ID del usuario autenticado.
        - threshold: Umbral de cantidad para considerar el stock como bajo (por defecto es 10).

        Levanta:
        - DBError: Si hay algún error durante la consulta en la base de datos.

        Retorna:
        - Una lista de diccionarios con los detalles de los productos con stock bajo,
        o un mensaje si no hay productos con stock bajo.
        """

        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute(
                'SELECT * FROM stock WHERE quantity <= %s AND user_id = %s',
                (threshold, user_id)
            )
            data = cursor.fetchall()
            cursor.close()
            connection.close()

            if data:
                low_stock_products = [Stock(row).to_json() for row in data]
                return low_stock_products
            
            return {"message": "No hay productos con stock bajo"}
        except Exception as e:
            cursor.close()
            connection.close()
            raise DBError(f"Error verificando stock bajo: {e}")

    @classmethod
    def get_stock_by_user(cls, user_id):
        """
        Obtiene el stock de todos los productos asociados a un usuario específico.

        Consulta la base de datos para obtener el ID, nombre y cantidad de cada producto en stock para el usuario autenticado.
        Retorna una lista de productos en formato JSON.

        Parámetros:
        - user_id: ID del usuario autenticado.

        Levanta:
        - DBError: Si hay algún error durante la consulta en la base de datos.

        Retorna:
        - Una lista de diccionarios con los detalles de los productos en stock, 
        o un mensaje si no hay productos en stock.
        """

        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            # Consulta que selecciona tanto el ID como el nombre del producto
            cursor.execute('''
                SELECT product_id, product_name, quantity
                FROM stock
                WHERE user_id = %s
            ''', (user_id,))
            
            data = cursor.fetchall()
            cursor.close()
            connection.close()

            if data:
                # Construcción de la lista de resultados
                all_stock = [
                    {
                        "product_id": row[0],
                        "product_name": row[1],
                        "quantity": row[2]
                    }
                    for row in data
                ]
                return all_stock
            
            return {"message": "No hay productos en stock"}
        except Exception as e:
            cursor.close()
            connection.close()
            raise DBError(f"Error obteniendo el stock: {e}")
