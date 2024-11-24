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
