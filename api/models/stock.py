from api.db.db_config import get_db_connection, DBError
from api import app

class Stock:
    schema = {
        "quantity": int  # Solo necesitamos validar 'quantity' en la entrada
    }

    @classmethod
    def validate(cls,data):
        if data == None or type(data) != dict:
            return False
        # Control: data contiene todas las claves?
        for key in cls.schema:
            if key not in data:
                return False
            # Control: cada valor es del tipo correcto?
            if type(data[key]) != cls.schema[key]:
                return False
        return True

    # Constructor base 
    def __init__(self, data):
        self.producto_id = data[0]
        self.quantity = data[1]

    # Conversión a objeto JSON
    def to_json(self):
        return {
            "product_id": self.producto_id,
            "quantity": self.quantity
        }

    @classmethod
    def update_stock(cls, user_id, product_id, new_quantity):
        """
        Actualiza la cantidad de productos en stock asociados a un usuario específico.
        """
        # Validación de cantidad
        if new_quantity <= 0:
            raise DBError("La cantidad debe ser mayor a 0")

        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            # Verificar la cantidad actual del producto
            cursor.execute(
                'SELECT quantity FROM stock WHERE product_id = %s AND user_id = %s',
                (product_id, user_id)
            )
            current_quantity = cursor.fetchone()
            
            if not current_quantity:
                raise DBError("El producto no existe o no pertenece al usuario")
            
            if current_quantity[0] == new_quantity:
                return {"message": "Stock no actualizado, esa cantidad es igual a la actual"}
            
            # Actualizar la cantidad del producto
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
        Obtiene todos los productos en stock.
        """
        connection = get_db_connection()
        cursor = connection.cursor()
        
        try:
            cursor.execute('SELECT * FROM stock WHERE user_id = %s', (user_id,))
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
