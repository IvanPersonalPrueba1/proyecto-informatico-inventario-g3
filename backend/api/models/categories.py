from api.db.db_config import get_db_connection, DBError
from api import app

class Category():
    schema = {
        "name": str,
        "descripcion": str  
    }

    @classmethod
    def validate(cls, data):
        #Valida los datos de la categoría.
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
        #Convierte la categoría a formato JSON.
        return {
            "id": self._id,
            "name": self._name,
            "descripcion": self._descripcion,  
        }

    @classmethod
    def get_categories(cls, user_id):
        #Obtiene todas las categorías para un usuario.
        with get_db_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM categories WHERE user_id = %s', (user_id,))
            data = cursor.fetchall()

            if not data:
                raise DBError("no hay datos aun")

            return [cls(fila).to_json() for fila in data]

    @classmethod
    def create_category(cls, user_id, data):
        #Crea una nueva categoría para un usuario.
        name = data.get("name")
        descripcion = data.get("descripcion") 

        with get_db_connection() as connection:
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

        return {"message": "Categoría creada exitosamente"}, 201

    @classmethod
    def update_category(cls, user_id, category_id, data):
        #Actualiza una categoría existente para un usuario.
        name = data.get("name")
        descripcion = data.get("descripcion")  

        with get_db_connection() as connection:
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

        return {"message": "Categoría actualizada exitosamente"}, 200

    @classmethod
    def delete_category(cls, user_id, category_id):
        # Elimina una categoría para un usuario.
        with get_db_connection() as connection:
            cursor = connection.cursor()
            try:
                # Verificar si la categoría existe
                cursor.execute('SELECT id FROM categories WHERE id = %s AND user_id = %s', (category_id, user_id))
                existing_category = cursor.fetchone()
                if not existing_category:
                    raise DBError("La categoría no existe para este usuario")

                # Asegurarse de que la categoría "None" esté configurada
                cursor.execute('SELECT id FROM categories WHERE name = "None"')
                none_category = cursor.fetchone()

                # Si no existe la categoría "None", puedes decidir crearla aquí
                if not none_category:
                    cursor.execute(
                        'INSERT INTO categories (name, descripcion, user_id) VALUES (%s, %s, %s)',
                        ('None', 'Categoría predeterminada para productos no categorizados', user_id)
                    )
                    connection.commit()
                    # Recuperar el ID de la categoría "None" después de crearla
                    cursor.execute('SELECT id FROM categories WHERE name = "None" AND user_id = %s', (user_id,))
                    none_category = cursor.fetchone()

                none_category_id = none_category[0]

                # Actualizar los productos para asignarlos a la categoría "None"
                cursor.execute(
                    'UPDATE products SET category_id = %s WHERE category_id = %s AND user_id = %s',
                    (none_category_id, category_id, user_id)
                )

                # Eliminar la categoría
                cursor.execute('DELETE FROM categories WHERE id = %s AND user_id = %s', (category_id, user_id))
                connection.commit()

            except Exception as e:
                raise DBError(f"Error al eliminar la categoría: {str(e)}")

        return {"message": "Categoría eliminada exitosamente"}, 200
