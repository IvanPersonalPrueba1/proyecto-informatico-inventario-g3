from api.db.db_config import get_db_connection, DBError
from api import app

class Category():
    schema = {
        "name": str,
        "descripcion": str
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
        self._id = data[0]
        self._name = data[1]
        self._descripcion = data[2]

    def to_json(self):
        return {
            "id": self._id,
            "name": self._name,
            "descripcion": self._descripcion,
        }
        
    @classmethod
    def get_categories(cls, user_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM categories WHERE user_id = %s', (user_id,))
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        
        if not data:
            raise DBError("No existe el recurso solicitado")

        return [cls(fila).to_json() for fila in data]

    @classmethod
    def create_category(cls, user_id, data):
        name = data.get("name")
        descripcion = data.get("descripcion")  

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # Verificar si el usuario existe
            cursor.execute('SELECT id FROM users WHERE id = %s', (user_id,))
            user = cursor.fetchone()
            if not user:
                raise DBError("El usuario no existe")

            # Verificar si ya existe una categoría con ese nombre
            cursor.execute('SELECT id FROM categories WHERE name = %s AND user_id = %s', (name, user_id))
            existing_category = cursor.fetchone()
            if existing_category:
                raise DBError("Ya existe una categoría con ese nombre para este usuario")

            # Insertar la nueva categoría
            cursor.execute('INSERT INTO categories (name, descripcion, user_id) VALUES (%s, %s, %s)', 
                           (name, descripcion, user_id))
            connection.commit()

        except Exception as e:
            raise DBError(f"Error al crear la categoría: {str(e)}")
        
        finally:
            cursor.close()
            connection.close()

        return {"message": "Categoría creada exitosamente"}, 201

    @classmethod
    def update_category(cls, user_id, category_id, data):
        name = data.get("name")
        descripcion = data.get("descripcion")

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # Verificar si la categoría existe para el usuario
            cursor.execute('SELECT id FROM categories WHERE id = %s AND user_id = %s', (category_id, user_id))
            existing_category = cursor.fetchone()
            if not existing_category:
                raise DBError("La categoría no existe para este usuario")

            # Actualizar la categoría
            cursor.execute(
                'UPDATE categories SET name = %s, descripcion = %s WHERE id = %s AND user_id = %s',
                (name, descripcion, category_id, user_id)
            )
            connection.commit()

        except Exception as e:
            raise DBError(f"Error al actualizar la categoría: {str(e)}")

        finally:
            cursor.close()
            connection.close()

        return {"message": "Categoría actualizada exitosamente"}, 200

    @classmethod
    def delete_category(cls, user_id, category_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # Verificar si la categoría existe para el usuario
            cursor.execute('SELECT id FROM categories WHERE id = %s AND user_id = %s', (category_id, user_id))
            existing_category = cursor.fetchone()
            if not existing_category:
                raise DBError("La categoría no existe para este usuario")

            # Eliminar la categoría
            cursor.execute('DELETE FROM categories WHERE id = %s AND user_id = %s', (category_id, user_id))
            connection.commit()

        except Exception as e:
            raise DBError(f"Error al eliminar la categoría: {str(e)}")

        finally:
            cursor.close()
            connection.close()

        return {"message": "Categoría eliminada exitosamente"}, 200
