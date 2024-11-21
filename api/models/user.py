from api.db.db_config import get_db_connection, DBError
from werkzeug.security import generate_password_hash, check_password_hash  
import jwt
import datetime
from api import app


app.config['SECRET_KEY'] = "clave_app"


class User():
    schema = {
        "username": str,
        "password" : str
    }


    @classmethod
    def validate(cls,data):
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
        self._username = data[1]
        self._password = data[2]


    def to_json(self):
        return {
            "id": self._id,
            "username": self._username,
            #"password": self._password
        } 
    
    @classmethod
    def register(cls, data):


        if not cls.validate(data):
            raise DBError({"message": "Campos/valores inválidos", "code": 400})
        
        username = data["username"]
        password = data["password"]

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM usuarios WHERE username = %s', (username,))
        row = cursor.fetchone()

        if row is not None:
            raise DBError({"message": "Ya existe un usuario con ese nombre", "code": 400})
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        cursor.execute('INSERT INTO usuarios (username, password) VALUES (%s, %s)', (username, hashed_password))
        connection.commit()


        cursor.execute('SELECT LAST_INSERT_ID()')
        row = cursor.fetchone()
        id = row[0]

        cursor.execute('SELECT * FROM usuarios WHERE id = %s', (id, ))
        nuevo = cursor.fetchone()
        cursor.close()
        connection.close()

        exp_timestamp = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)).timestamp()
        token = jwt.encode({
            'username': username,
            'id': id,
            'exp': exp_timestamp
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return {
            "user": User(nuevo).to_json(),
            "token": token
        }
            
    @classmethod
    def login(cls, auth):
        if not auth or not auth.username or not auth.password:
            raise DBError({"message": "No autorizado", "code": 401})

        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT id, username, password FROM usuarios WHERE username = %s', (auth.username,))
        row = cursor.fetchone()

        if not row or not check_password_hash(row[2], auth.password):
            raise DBError({"message": "No autorizado", "code": 401})

        exp_timestamp = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)).timestamp()

        token = jwt.encode({
            'username': auth.username,
            'id': row[0],
            'exp': exp_timestamp
        }, app.config['SECRET_KEY'], algorithm="HS256")

        return {"token": token, "username": auth.username, "id": row[0]}
