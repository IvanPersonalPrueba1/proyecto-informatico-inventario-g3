from api.db.db_config import get_db_connection, DBError
from flask import request, jsonify
from api import app

class Supplier:
    # Esquema de validación para los datos de proveedor
    schema = {
        "name_supplier": str,
        "phone": str,
        "mail": str
    }

    @classmethod
    def validate(cls, data):
        """ 
        Valida los datos del proveedor contra el esquema definido. 

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

    # Constructor base (se tiene en cuenta el orden de las columnas en la base de datos!)
    def __init__(self, data):
        """ 
        Inicializa un objeto Supplier con los datos proporcionados. 

        Parámetros:
        - data: Tupla con los datos del proveedor en el siguiente orden:
                (id, name_supplier, phone, mail)
        """

        self.id = data[0]
        self.name_supplier = data[1]
        self.phone = data[2]
        self.mail = data[3]
    
    # Conversión a objeto JSON
    def to_json(self):
        """ 
        Convierte el objeto Supplier a un diccionario JSON. 

        Retorna:
        - Diccionario con los datos del proveedor en formato JSON.
        """
        
        return {
            "id": self.id,
            "name_supplier": self.name_supplier,
            "phone": self.phone,
            "mail": self.mail,
        }

    @classmethod
    def create_supplier(cls, user_id, data):
        """ 
        Crea un nuevo proveedor asociado a un usuario. 
        Valida los datos del proveedor, verifica que no existan duplicados y luego lo inserta en la base de datos. 
        Retorna el proveedor creado en formato JSON. 
        
        Parámetros: 
        - user_id: ID del usuario al que se asociará el proveedor. 
        - data: Diccionario con los datos del proveedor (name_supplier, phone, mail). 
        
        Levanta: - DBError: Si los datos no son válidos o si hay duplicados en la base de datos. 
        """
        
        # Validar los datos del proveedor
        if not cls.validate(data):
            raise DBError("Campos/valores inválidos")

        connection = get_db_connection()
        cursor = connection.cursor()

        # Extraer datos del proveedor
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
        """
        Asocia un producto a un proveedor para un usuario autenticado.

        Verifica que el proveedor y el producto existen y pertenecen al usuario autenticado,
        que la asociación no existe ya, y luego inserta la asociación en la base de datos.

        Parámetros:
        - user_id: ID del usuario autenticado.
        - supplier_id: ID del proveedor.
        - product_id: ID del producto.

        Levanta:
        - DBError: Si el proveedor o el producto no existen, no pertenecen al usuario autenticado,
        o si la asociación ya existe.
        """

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
            raise DBError(f"{e}")


    @classmethod
    def get_proveedores_by_producto(cls, user_id, product_id):
        """
        Obtiene el ID y el nombre de todos los proveedores asociados a un usuario para un producto específico.

        Verifica que el producto pertenece al usuario autenticado y luego obtiene los proveedores asociados a ese producto.
        Retorna una lista de proveedores en formato JSON.

        Parámetros:
        - user_id: ID del usuario autenticado.
        - product_id: ID del producto.

        Levanta:
        - DBError: Si el producto no existe o no pertenece al usuario.

        Retorna:
        - Una lista de diccionarios con los detalles de los proveedores, o un mensaje si no hay proveedores asociados.
        """
        
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
                SELECT suppliers.id, suppliers.name_supplier, suppliers.phone, suppliers.mail, suppliers.user_id 
                FROM suppliers
                JOIN suppliers_products ON suppliers.id = suppliers_products.supplier_id
                WHERE suppliers_products.product_id = %s AND suppliers.user_id = %s
                ''',
                (product_id, user_id)
            )
            suppliers = cursor.fetchall()

            if not suppliers:
                return {"message": "El proveedor seleccionado no posee ese producto específico"}

            # Transformar los resultados en formato JSON
            supplier_json = [
                {
                    "id": i[0],
                    "name_supplier": i[1],
                    "phone": i[2],
                    "mail": i[3],
                    "user_id": i[4]
                }
                for i in suppliers
            ]

            cursor.close()
            connection.close()

            return supplier_json
        except Exception as e:
            cursor.close()
            connection.close()
            raise DBError(f"Error obteniendo los proveedores: {e}")


    @classmethod
    def get_suppliers_by_user(cls, user_id):
        """
        Obtiene el ID y el nombre de todos los proveedores asociados a un usuario específico.

        Consulta la base de datos para obtener los proveedores que están asociados al usuario autenticado.
        Retorna una lista de proveedores en formato JSON.

        Parámetros:
        - user_id: ID del usuario autenticado.

        Levanta:
        - DBError: Si hay algún error en la consulta de la base de datos.

        Retorna:
        - Una lista de diccionarios con los detalles de los proveedores, o un mensaje si no hay proveedores asociados.
        """

        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # Consultar IDs y nombres de los proveedores asociados al usuario
            cursor.execute(
                '''
                SELECT id, name_supplier 
                FROM suppliers 
                WHERE user_id = %s
                ''',
                (user_id,)
            )
            suppliers = cursor.fetchall()
            cursor.close()
            connection.close()

            if suppliers:
                supplier_list = [
                    {"id": row[0], "name_supplier": row[1]}
                    for row in suppliers
                ]
                return supplier_list
            
            return {"message": "No hay proveedores asociados a este usuario"}
        except Exception as e:
            cursor.close()
            connection.close()
            raise DBError(f"Error obteniendo los proveedores: {e}")
