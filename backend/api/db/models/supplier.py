class Supplier:
    @classmethod
    def add(cls, data, connection):
        """Agrega un nuevo proveedor."""
        query = "INSERT INTO suppliers (name, contact_info) VALUES (%s, %s)"
        values = (data["name"], data["contact_info"])
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        return {"message": "Proveedor agregado exitosamente."}, 201

    @classmethod
    def list_all(cls, connection):
        """Lista todos los proveedores."""
        query = "SELECT * FROM suppliers"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows, 200

    @classmethod
    def update(cls, supplier_id, data, connection):
        """Actualiza un proveedor."""
        query = "UPDATE suppliers SET name = %s, contact_info = %s WHERE id = %s"
        values = (data["name"], data["contact_info"], supplier_id)
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        return {"message": "Proveedor actualizado exitosamente."}, 200

    @classmethod
    def delete(cls, supplier_id, connection):
        """Elimina un proveedor."""
        query = "DELETE FROM suppliers WHERE id = %s"
        cursor = connection.cursor()
        cursor.execute(query, (supplier_id,))
        connection.commit()
        cursor.close()
        return {"message": "Proveedor eliminado exitosamente."}, 200
