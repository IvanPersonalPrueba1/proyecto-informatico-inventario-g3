from werkzeug.security import generate_password_hash, check_password_hash
from backend.api.db.db_connector import get_db_connection
import jwt
import datetime

class User:
    @classmethod
    def validate(cls, data):
        """Valida los datos del usuario contra el esquema definido."""
        if not data or type(data) != dict:
            return False
        required_keys = ["username", "password"]
        for key in required_keys:
            if key not in data:
                return False
        return True

    @classmethod
    def register(cls, data):
        """Registra un nuevo usuario en la base de datos."""
        if not cls.validate(data):
            return {"message": "Datos inválidos"}, 400
        
        username = data["username"]
        password = data["password"]
        
        connection = get_db_connection()  # Conexión creada dentro del método
        cursor = connection.cursor()
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        row = cursor.fetchone()
        
        if row:
            return {"message": "Usuario ya existe"}, 400
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, hashed_password))
        connection.commit()
        
        cursor.execute('SELECT LAST_INSERT_ID()')
        id = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        
        return {"id": id, "username": username}, 201

    @classmethod
    def login(cls, auth):
        """Autentica al usuario y genera un token JWT."""
        username = auth.get("username")
        password = auth.get("password")
        
        if not username or not password:
            return {"message": "Datos incorrectos"}, 401
        
        connection = get_db_connection()  # Conexión creada dentro del método
        cursor = connection.cursor()
        cursor.execute('SELECT id, username, password FROM users WHERE username = %s', (username,))
        row = cursor.fetchone()
        
        if not row or not check_password_hash(row[2], password):
            return {"message": "Usuario o contraseña incorrectos"}, 401
        
        exp_timestamp = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=6)).timestamp()
        token = jwt.encode({
            'username': username,
            'id': row[0],
            'exp': exp_timestamp
        }, "clave_app", algorithm="HS256")
        
        cursor.close()
        connection.close()
        
        return {"token": token, "username": username, "id": row[0]}, 200
