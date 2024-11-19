from api.db.db_config import get_db_connection, DBError
import logging

class Stock:
    schema = {
        "quantity": int  # Solo necesitamos validar 'quantity' en la entrada
    }

    @classmethod
    def validate(cls, data):
        if data is None or type(data) != dict:
            logging.error(f"Validation failed: data is None or not a dict. Data: {data}")
            return False
        for key in cls.schema:
            if key not in data:
                logging.error(f"Validation failed: key '{key}' not in data. Data: {data}")
                return False
            if type(data[key]) != cls.schema[key]:
                logging.error(f"Validation failed: key '{key}' type mismatch. Expected {cls.schema[key]}, got {type(data[key])}. Data: {data}")
                return False
        return True

    def __init__(self, data):
        self.producto_id = data[0]
        self.cantidad = data[1]

    def to_json(self):
        return {
            "producto_id": self.producto_id,
            "cantidad": self.cantidad
        }

    @classmethod
    def update_stock(cls, producto_id, new_quantity):
        """
        Actualiza la cantidad de productos en stock.
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute(
                'UPDATE stock SET cantidad = %s WHERE producto_id = %s',
                (new_quantity, producto_id)
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
    def check_low_stock(cls, threshold=10):
        """
        Verifica si algún producto tiene stock bajo.
        Retorna una lista de productos con stock bajo.
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute('SELECT * FROM stock WHERE cantidad <= %s', (threshold,))
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
    def get_all_stock(cls):
        """
        Obtiene todos los productos en stock.
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute('SELECT * FROM stock')
            data = cursor.fetchall()
            cursor.close()
            connection.close()

            if data:
                all_stock = [Stock(row).to_json() for row in data]
                return all_stock
            
            return {"message": "No hay productos en stock"}
        except Exception as e:
            cursor.close()
            connection.close()
            raise DBError(f"Error obteniendo el stock: {e}")