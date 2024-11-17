from api.db.db_config import get_db_connection, DBError
from api import app

class Category():
    schema = {
        "name": str
    }

    @classmethod
    def validate(cls, data):
        if data == None or type(data) != dict:
            return False
        for key in cls.schema:
            if key not in data:
                return False
            if type(data[key]) != cls.schema[key]:
                return False
        return True

    def __init__(self, data):
        self._id = data[0]
        self._name = data[1]

    def to_json(self):
        return {
            "id": self._id,
            "name": self._name
        }

    @classmethod
    def get_categories(cls):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM categories')
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        
        if len(data) > 0:
            lista = []
            for fila in data:
                objeto = Category(fila).to_json()
                lista.append(objeto)
            return lista
        
        raise DBError("No existe el recurso solicitado")
