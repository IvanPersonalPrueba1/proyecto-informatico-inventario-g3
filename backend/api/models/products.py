from api.db.db_config import get_db_connection, DBError
from api import app

class Product():
    schema = {
        "name": str,
        "price": (int, float),  
        "category_id": (int, type(None)),
    }

    @classmethod
    def validate(cls, data):
        if not isinstance(data, dict):
            return False
        
        for key, value_type in cls.schema.items():
            value = data.get(key)
            # Verifica que el tipo de dato coincida y permite que category_id sea None
            if key == "category_id":
                if value is not None and not isinstance(value, int):
                    return False
            else:
                if not isinstance(value, value_type):
                    return False
            
            # Validaciones adicionales
            if key == "price":
                if value <= 0:
                    return False  # Asegura que el precio sea positivo
            
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
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT id, name, price, category_id FROM products WHERE user_id = %s', (user_id,))
                data = cursor.fetchall()

        if not data:
            raise DBError("no hay datos aun")

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
        category_id = data.get("category_id", None)
        
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    # Verificar si ya existe un producto con el mismo nombre para este usuario
                    cursor.execute(
                        'SELECT id FROM products WHERE name = %s AND user_id = %s',
                        (name, user_id)
                    )
                    existing_product = cursor.fetchone()
                    if existing_product:
                        raise DBError("No puedes crear el producto: ya existe un producto con ese nombre para este usuario.")

                    # Verificar si la categoría existe
                    if category_id is not None:
                        cursor.execute(
                            'SELECT id FROM categories WHERE id = %s AND user_id = %s', 
                            (category_id, user_id)
                        )
                        category_exists = cursor.fetchone()
                        if not category_exists:
                            raise DBError("La categoría especificada no existe para este usuario.")

                    # Crear producto
                    cursor.execute(
                        'INSERT INTO products (name, price, category_id, user_id) VALUES (%s, %s, %s, %s)', 
                        (name, price, category_id if category_id else None, user_id)
                    )
                    connection.commit()

                except DBError as e:
                    raise DBError(f"Error al crear el producto: {str(e)}")
                except Exception as e:
                    raise DBError(f"Error interno del servidor: {str(e)}")

        return {"message": "Producto creado exitosamente"}, 201

    @classmethod
    def update_product(cls, user_id, product_id, data):
        name = data.get("name")
        price = data.get("price")
        category_id = data.get("category_id", None)

        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    if category_id is not None:
                        cursor.execute(
                            'SELECT id FROM categories WHERE id = %s AND user_id = %s', (category_id, user_id)
                        )
                        category_exists = cursor.fetchone()
                        if not category_exists:
                            raise DBError("La categoría especificada no existe para este usuario")

                    cursor.execute(
                        'UPDATE products SET name = %s, price = %s, category_id = %s WHERE id = %s AND user_id = %s',
                        (name, price, category_id, product_id, user_id)
                    )
                    connection.commit()

                except DBError as e:
                    raise DBError(f"Error al actualizar el producto: {str(e)}")

        return {"message": "Producto actualizado exitosamente"}, 200

    @classmethod
    def delete_product(cls, user_id, product_id):
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                try:
                    # Verificar si el producto existe para el usuario
                    cursor.execute('SELECT id FROM products WHERE id = %s AND user_id = %s', (product_id, user_id))
                    existing_product = cursor.fetchone()
                    if not existing_product:
                        raise DBError("El producto no existe para este usuario")

                    # Eliminar el producto
                    cursor.execute('DELETE FROM products WHERE id = %s AND user_id = %s', (product_id, user_id))
                    connection.commit()

                except DBError as e:
                    raise DBError(f"Error al eliminar el producto: {str(e)}")

        return {"message": "Producto eliminado exitosamente"}, 200

    @classmethod
    def get_product_by_id(cls, user_id, product_id):
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT id, name, price, category_id FROM products WHERE id = %s AND user_id = %s', (product_id, user_id))
                data = cursor.fetchone()

        if not data:
            raise DBError("No existe el producto solicitado para este usuario")

        return {
            "id": data[0],
            "name": data[1],
            "price": data[2],
            "category_id": data[3]
        }

    @classmethod
    def get_products_by_category_id(cls, user_id, category_id):
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                # Interpretar category_id igual a 0 como None
                if category_id == 0:
                    category_id = None

                if category_id is not None:
                    cursor.execute(
                        'SELECT id, name, price, category_id FROM products WHERE category_id = %s AND user_id = %s',
                        (category_id, user_id)
                    )
                else:
                    cursor.execute(
                        'SELECT id, name, price, category_id FROM products WHERE category_id IS NULL AND user_id = %s',
                        (user_id,)
                    )

                data = cursor.fetchall()

        # Convertir los datos a un formato de respuesta JSON
        return [
            {
                "id": row[0],
                "name": row[1],
                "price": row[2],
                "category_id": row[3]
            } for row in data
        ] if data else [] 