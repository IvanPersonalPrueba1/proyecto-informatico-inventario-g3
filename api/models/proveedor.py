from api.db.db_config import get_db_connection, DBError
from api import app

class Proveedor:
    schema = {
        "nombre": str,
        "telefono": str,
        "mail": str,
        "id_usuario": int
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
        self.id = data[0]
        self.nombre = data[1]
        self.telefono = data[2]
        self.mail = data[3]
        self.id_usuario = data[4]

    def to_json(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "telefono": self.telefono,
            "mail": self.mail,
            "id_usuario": self.id_usuario
        }

    @classmethod
    def create_proveedor(cls, id_user, data):
        if not cls.validate(data):
            raise DBError("Campos/valores inválidos")

        connection = get_db_connection()
        cursor = connection.cursor()

        id_usuario = data["id_usuario"]

        # Verificar que el id_usuario coincide con el id_user autenticado
        if int(id_user) != int(id_usuario):
            raise DBError("El usuario no coincide con el ID autenticado")

        nombre = data["nombre"]
        telefono = data["telefono"]
        mail = data["mail"]

        try:
            # Insertar proveedor
            cursor.execute(
                '''
                INSERT INTO proveedores (nombre, telefono, mail, id_usuario) 
                VALUES (%s, %s, %s, %s)
                ''',
                (nombre, telefono, mail, id_usuario)
            )
            connection.commit()

            # Obtener ID del proveedor recién creado
            cursor.execute('SELECT LAST_INSERT_ID()')
            row = cursor.fetchone()
            id = row[0]

            # Recuperar y devolver el proveedor creado
            cursor.execute('SELECT * FROM proveedores WHERE id = %s', (id,))
            nuevo = cursor.fetchone()

            cursor.close()
            connection.close()

            return Proveedor(nuevo).to_json()
        except Exception as e:
            connection.rollback()
            cursor.close()
            connection.close()
            raise DBError(f"Error creando el proveedor: {e}")

    @classmethod
    def add_producto_to_proveedor(cls, id_user, id_proveedor, id_producto):
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # Verificar que el proveedor pertenece al usuario autenticado
            cursor.execute(
                '''
                SELECT id FROM proveedores WHERE id = %s AND id_usuario = %s
                ''',
                (id_proveedor, id_user)
            )
            if not cursor.fetchone():
                raise DBError("Proveedor no encontrado o no pertenece al usuario")

            # Verificar que el producto pertenece al usuario autenticado
            cursor.execute(
                '''
                SELECT id FROM productos WHERE id = %s AND id_usuario = %s
                ''',
                (id_producto, id_user)
            )
            if not cursor.fetchone():
                raise DBError("Producto no encontrado o no pertenece al usuario")

            # Asociar el producto al proveedor
            cursor.execute(
                '''
                INSERT INTO proveedores_productos (id_proveedor, id_producto) 
                VALUES (%s, %s)
                ''',
                (id_proveedor, id_producto)
            )
            connection.commit()

            cursor.close()
            connection.close()
        except Exception as e:
            connection.rollback()
            cursor.close()
            connection.close()
            raise DBError(f"Error asociando producto al proveedor: {e}")



    @classmethod
    def get_proveedores_by_producto(cls, id_user, id_producto):
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # Verificar que el producto pertenece al usuario autenticado
            cursor.execute(
                '''
                SELECT id 
                FROM productos 
                WHERE id = %s AND id_usuario = %s
                ''',
                (id_producto, id_user)
            )
            producto = cursor.fetchone()
            if not producto:
                raise DBError("Producto no encontrado o no pertenece al usuario")

            # Obtener los proveedores asociados al producto
            cursor.execute(
                '''
                SELECT p.id, p.nombre, p.telefono, p.mail, p.id_usuario 
                FROM proveedores p
                JOIN proveedores_productos pp ON p.id = pp.id_proveedor
                WHERE pp.id_producto = %s AND p.id_usuario = %s
                ''',
                (id_producto, id_user)
            )
            proveedores = cursor.fetchall()

            # Transformar los resultados en formato JSON
            proveedores_json = [
                {
                    "id": p[0],
                    "nombre": p[1],
                    "telefono": p[2],
                    "mail": p[3],
                    "id_usuario": p[4]
                }
                for p in proveedores
            ]

            cursor.close()
            connection.close()

            return proveedores_json
        except Exception as e:
            cursor.close()
            connection.close()
            raise DBError(f"Error obteniendo los proveedores: {e}")
