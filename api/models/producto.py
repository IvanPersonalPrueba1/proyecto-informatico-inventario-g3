from api.db.db_config import get_db_connection, DBError

class Product():
    schema = {
        "name": str,
        "price": (int, float),  
        "category_id": int  
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
        self._id = None 
        try:
            self._name = data["name"]
            self._price = data["price"]
            self._category_id = data["category_id"]
        except KeyError as e:
            raise ValueError(f"Falta la clave esperada: {e}")

        
    def to_json(self):
        return {
            "id": self._id,
            "name": self._name,
            "price": self._price,
            "category_id": self._category_id
        }

    @classmethod
    def get_products_by_user(cls, user_id):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT id, name, price, category_id FROM products WHERE user_id = %s', (user_id,))
        data = cursor.fetchall()
        cursor.close()
        connection.close()

        if not data:
            raise DBError("No existe el recurso solicitado")

        return [
            {
                "id": fila[0],
                "name": fila[1],  
                "price": fila[2],  
                "category_id": fila[3]  
            }
            for fila in data
        ]
