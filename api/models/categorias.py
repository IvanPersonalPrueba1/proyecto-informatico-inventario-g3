from api.db.db_config import get_db_connection, DBError
from api import app
from api.models.base import BaseModel

class Category(BaseModel):
    schema = {
        "name": str
    }

    def __init__(self, data):
        self._id = data[0]
        self._name = data[1]


    @classmethod
    def get_categories(cls, usuario_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM categorias WHERE usuario_id = %s', (usuario_id,))
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        
        if not data:
            raise DBError("No existe el recurso solicitado")

        return [cls(fila).to_json() for fila in data]
