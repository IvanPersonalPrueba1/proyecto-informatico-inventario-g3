from api.db.db_config import get_db_connection, DBError
from flask import request, jsonify
from api import app

class Supplier:
    schema = {
        "name_supplier": str,
        "phone": str,
        "mail": str
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
        self.name_supplier = data[1]
        self.phone = data[2]
        self.mail = data[3]

    def to_json(self):
        return {
            "id": self.id,
            "name_supplier": self.name_supplier,
            "phone": self.phone,
            "mail": self.mail,
        }

    @classmethod
    def create_supplier(cls, user_id, data):
        if not cls.validate(data):
            raise DBError("Campos/valores inválidos")

        connection = get_db_connection()
        cursor = connection.cursor()

        name_supplier = data["name_supplier"]
        phone = data["phone"]
        mail = data["mail"]

        try:
            # Verificar que el proveedor no existe
            cursor.execute(
                '''
                SELECT id FROM suppliers WHERE name_supplier = %s
                ''',
                (name_supplier,)
            )
            if cursor.fetchone():
                raise DBError("El proveedor ya existe")

            # Verificar que el número de teléfono no está registrado
            cursor.execute(
                '''
                SELECT id FROM suppliers WHERE phone = %s
                ''',
                (phone,)
            )
            if cursor.fetchone():
                raise DBError("El número de teléfono ya se encuentra registrado en nuestra base de datos")

            # Verificar que el correo electrónico no está registrado
            cursor.execute(
                '''
                SELECT id FROM suppliers WHERE mail = %s
                ''',
                (mail,)
            )
            if cursor.fetchone():
                raise DBError("El correo electrónico ya se encuentra registrado en nuestra base de datos")

            # Insertar proveedor
            cursor.execute(
                '''
                INSERT INTO suppliers (name_supplier, phone, mail, user_id) 
                VALUES (%s, %s, %s, %s)
                ''',
                (name_supplier, phone, mail, user_id)
            )
            connection.commit()

            # Obtener ID del proveedor recién creado
            cursor.execute('SELECT LAST_INSERT_ID()')
            row = cursor.fetchone()
            id = row[0]

            # Recuperar y devolver el proveedor creado
            cursor.execute('SELECT * FROM suppliers WHERE id = %s', (id,))
            nuevo = cursor.fetchone()

            cursor.close()
            connection.close()

            return Supplier(nuevo).to_json()
        except Exception as e:
            connection.rollback()
            cursor.close()
            connection.close()
            raise DBError(f"Error creando el proveedor: {e}")




    @classmethod
    def add_product_to_supplier(cls, user_id, supplier_id, product_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # Verificar que el proveedor existe y pertenece al usuario autenticado
            cursor.execute(
                '''
                SELECT id, user_id FROM suppliers WHERE id = %s AND user_id = %s
                ''',
                (supplier_id, user_id)
            )
            supplier = cursor.fetchone()
            if not supplier:
                raise DBError("El proveedor no existe o no pertenece al usuario autenticado")

            # Verificar que el producto existe y pertenece al usuario autenticado
            cursor.execute(
                '''
                SELECT id, user_id FROM products WHERE id = %s AND user_id = %s
                ''',
                (product_id, user_id)
            )
            product = cursor.fetchone()
            if not product:
                raise DBError("El producto no existe o no pertenece al usuario autenticado")

            # Verificar que el producto no esté ya asociado al proveedor
            cursor.execute(
                '''
                SELECT supplier_id, product_id FROM suppliers_products WHERE supplier_id = %s AND product_id = %s AND user_id = %s
                ''',
                (supplier_id, product_id, user_id)
            )
            if cursor.fetchone():
                raise DBError("El producto ya está asociado al proveedor")

            # Asociar el producto al proveedor
            cursor.execute(
                '''
                INSERT INTO suppliers_products (supplier_id, product_id, user_id) 
                VALUES (%s, %s, %s)
                ''',
                (supplier_id, product_id, user_id)
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
    def get_proveedores_by_producto(cls, user_id, product_id):
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # Verificar que el producto pertenece al usuario autenticado
            cursor.execute(
                '''
                SELECT id 
                FROM products 
                WHERE id = %s AND user_id = %s
                ''',
                (product_id, user_id)
            )
            product = cursor.fetchone()
            if not product:
                raise DBError("Producto no encontrado o no pertenece al usuario")

            # Obtener los proveedores asociados al producto
            cursor.execute(
                '''
                SELECT p.id, p.name_supplier, p.phone, p.mail, p.user_id 
                FROM suppliers p
                JOIN suppliers_products pp ON p.id = pp.supplier_id
                WHERE pp.product_id = %s AND p.user_id = %s
                ''',
                (product_id, user_id)
            )
            suppliers = cursor.fetchall()

            if not suppliers:
                return {"message": "El proveedor seleccionado no posee ese producto específico"}

            # Transformar los resultados en formato JSON
            supplier_json = [
                {
                    "id": p[0],
                    "name_supplier": p[1],
                    "phone": p[2],
                    "mail": p[3],
                    "user_id": p[4]
                }
                for p in suppliers
            ]

            cursor.close()
            connection.close()

            return supplier_json
        except Exception as e:
            cursor.close()
            connection.close()
            raise DBError(f"Error obteniendo los proveedores: {e}")

