from api.models.base import BaseModel
from api.db.db_config import get_db_connection, DBError

class Product(BaseModel):
    schema = {"name": str, "price": int}

    def __init__(self, data):
        self._id = data[0]
        self._name = data[1]
        self._price = data[2]
        self._id_user = data[3]

    @classmethod
    def get_products_by_user(cls, id_user):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM products WHERE id_user = %s', (id_user,))
        data = cursor.fetchall()
        cursor.close()
        connection.close()

        if not data:
            raise DBError("No existe el recurso solicitado")

        return [cls(fila).to_json() for fila in data]
