from api.db.db_config import get_db_connection, DBError
from werkzeug.security import generate_password_hash, check_password_hash  # Para manejo de hash de contraseñas
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
        # Control: data contiene todas las claves?
        for key in cls.schema:
            if key not in data:
                return False
            # Control: cada valor es del tipo correcto?
            if type(data[key]) != cls.schema[key]:
                return False
        return True
    
    # Constructor base (se tiene en cuenta el orden de las columnas en la base de datos!)
    def __init__(self, data):
        self._id = data[0]
        self._username = data[1]
        self._password = data[2]


    # Conversión a objeto JSON
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


        # Buscar si existe un usuario con el mismo nombre
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        row = cursor.fetchone()

        
        if row is not None:
            raise DBError({"message": "Ya existe un usuario con ese nombre", "code": 400})
        
        # Generar el hash de la contraseña
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Guardar el usuario en la base de datos con la contraseña hasheada        
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        connection.commit()
        

        #obtener el id del registro creado
        cursor.execute('SELECT LAST_INSERT_ID()')
        row = cursor.fetchone()
        id = row[0]


        # Recuperar el objeto creado
        cursor.execute('SELECT * FROM users WHERE id = %s', (id, ))
        nuevo = cursor.fetchone()
        cursor.close()
        connection.close()
        return User(nuevo).to_json()
    
    @classmethod
    def login(cls, auth):
        
        if not auth or not auth.username or not auth.password:
            raise DBError({"message": "No autorizado", "code": 401})


        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Buscar el usuario por nombre de usuario
        cursor.execute('SELECT id, username, password FROM users WHERE username = %s', (auth.username,))
        row = cursor.fetchone()


        # row[2] contiene el hash de la contraseña
        if not row or not check_password_hash(row[2], auth.password): 
            raise DBError({"message": "No autorizado", "code": 401})


        # Obtener la hora actual en UTC y convertirla a un timestamp
        exp_timestamp = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=12)).timestamp()
        
        # Generar token JWT
        token = jwt.encode({
            'username': auth.username,
            'id': row[0],
            'exp': exp_timestamp
        }, app.config['SECRET_KEY'], algorithm = "HS256")
        return {"token": token, "username": auth.username, "id": row[0]}