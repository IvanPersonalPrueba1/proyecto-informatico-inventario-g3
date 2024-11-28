from api.db.db_config import get_db_connection, DBError

class Product():
    schema = {
        "name": str,
        "price": (int, float),  
        "category_id": int  
    }

    @classmethod
    def validate(cls, data):
        if data is None or not isinstance(data, dict):
            return False
        for key in cls.schema:
            if key not in data:
                return False
            if not isinstance(data[key], cls.schema[key]):
                return False
        return True

    def __init__(self, data):
        self._id = None 
        try:
            self._name = data["name"]
            self._price = data["price"]
            self._category_id = data["category_id"]
        except KeyError as e:
            raise ValueError(f"Falta la clave esperada: {e}")

    def to_json(self):
        return {
            "id": self._id,
            "name": self._name,
            "price": self._price,
            "category_id": self._category_id
        }

    @classmethod
    def get_products_by_user(cls, user_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT id, name, price, category_id FROM products WHERE user_id = %s', (user_id,))
        data = cursor.fetchall()
        cursor.close()
        connection.close()

        if not data:
            raise DBError("No existe el recurso solicitado")

        return [
            {
                "id": fila[0],
                "name": fila[1],  
                "price": fila[2],  
                "category_id": fila[3]  
            }
            for fila in data
        ]

    @classmethod
    def create_product(cls, user_id, data):
        name = data.get("name")
        price = data.get("price")
        category_id = data.get("category_id")

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # Verificar si el producto ya existe
            cursor.execute('SELECT id FROM products WHERE user_id = %s AND name = %s', (user_id, name))
            existing_product = cursor.fetchall()
            if existing_product:
                raise DBError("El producto ya existe para este usuario")

            # Crear el nuevo producto
            cursor.execute(
                'INSERT INTO products (name, price, category_id, user_id) VALUES (%s, %s, %s, %s)', 
                (name, price, category_id, user_id)
            )
            connection.commit()

        except Exception as e:
            raise DBError(f"Error al crear el producto: {str(e)}")

        finally:
            cursor.close()
            connection.close()

        return {"message": "Producto creado exitosamente"}, 201

    @classmethod
    def update_product(cls, user_id, product_id, data):
        name = data.get("name")
        price = data.get("price")
        category_id = data.get("category_id")

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # Verificar si el producto existe para el usuario
            cursor.execute('SELECT id FROM products WHERE id = %s AND user_id = %s', (product_id, user_id))
            existing_product = cursor.fetchone()
            if not existing_product:
                raise DBError("El producto no existe para este usuario")

            # Actualizar el producto
            cursor.execute(
                'UPDATE products SET name = %s, price = %s, category_id = %s WHERE id = %s AND user_id = %s',
                (name, price, category_id, product_id, user_id)
            )
            connection.commit()

        except Exception as e:
            raise DBError(f"Error al actualizar el producto: {str(e)}")

        finally:
            cursor.close()
            connection.close()

        return {"message": "Producto actualizado exitosamente"}, 200

    @classmethod
    def delete_product(cls, user_id, product_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # Verificar si el producto existe para el usuario
            cursor.execute('SELECT id FROM products WHERE id = %s AND user_id = %s', (product_id, user_id))
            existing_product = cursor.fetchone()
            if not existing_product:
                raise DBError("El producto no existe para este usuario")

            # Eliminar el producto
            cursor.execute('DELETE FROM products WHERE id = %s AND user_id = %s', (product_id, user_id))
            connection.commit()

        except Exception as e:
            raise DBError(f"Error al eliminar el producto: {str(e)}")

        finally:
            cursor.close()
            connection.close()

        return {"message": "Producto eliminado exitosamente"}, 200

    @classmethod
    def get_product_by_id(cls, user_id, product_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute('SELECT id, name, price, category_id FROM products WHERE id = %s AND user_id = %s', (product_id, user_id))
        data = cursor.fetchone()
        cursor.close()
        connection.close()

        if not data:
            raise DBError("No existe el producto solicitado para este usuario")

        return {
            "id": data[0],
            "name": data[1],
            "price": data[2],
            "category_id": data[3]
        }
