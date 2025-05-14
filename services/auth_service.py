import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy import select
from config.db import engine
from model.users import users
from werkzeug.security import check_password_hash
from fastapi.security import OAuth2PasswordBearer
from pprint import pprint


SECRET_KEY = "mi_clave_secreta_super_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/login/user")

def create_access_token(data: dict):
    """Genera un token JWT"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    """Verifica el token JWT y devuelve los datos del usuario"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")

def get_current_user(token: str):
    """Obtiene los datos del usuario actual a partir del token"""
    payload = verify_token(token)
    username = payload.get("sub")
    user_id = payload.get("id_user")

    if username is None or user_id is None:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    return {"username": username, "id_user": user_id}

def authenticate_user(username: str, password: str):
    """Verifica el usuario y la contraseña"""
    with engine.begin() as connection:
        result = connection.execute(select(users).where(users.c.username == username)).first()
        if result is None:
            return None

        user_data = dict(result._mapping)
        print("Usuario encontrado:")
        pprint(user_data)

        print(f"Comparando password enviada: {password}")
        print(f"Contra hash guardado: {user_data['password']}")

        if not check_password_hash(user_data["password"], password):
            print("Contraseña incorrecta")
            return None
        print("Contraseña válida")
        return user_data
