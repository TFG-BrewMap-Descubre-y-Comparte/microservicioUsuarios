from sqlalchemy import select
from config.db import engine
from model.users import users
from werkzeug.security import generate_password_hash

def get_all_users():
    """Obtiene todos los usuarios de la base de datos"""
    with engine.begin() as connection:
        result = connection.execute(select(users))
        return [dict(row._mapping) for row in result]

def get_user_by_id(id_user: str):
    """Obtiene un usuario por ID"""
    with engine.begin() as connection:
        result = connection.execute(select(users).where(users.c.id_user == id_user)).first()
        if result:
            return dict(result._mapping)
        return None

def create_user(data_user: dict):
    """Crea un nuevo usuario en la base de datos"""
    # Hasheamos solo aquí
    hashed_password = generate_password_hash(data_user["password"], method="pbkdf2:sha256", salt_length=30)
    data_user["password"] = hashed_password
    
    with engine.begin() as connection:
        result = connection.execute(users.insert().values(data_user))
        return result
        
def update_user(id_user: int, data_user: dict):
    """Actualiza los datos de un usuario existente"""
    if "password" in data_user:
        data_user["password"] = generate_password_hash(data_user["password"], method="pbkdf2:sha256", salt_length=30)
    
    with engine.begin() as connection:
        result = connection.execute(
            users.update().where(users.c.id_user == id_user).values(data_user)
        )
        return result

def delete_user(id_user: int):
    """Elimina un usuario de la base de datos"""
    with engine.begin() as connection:
        result = connection.execute(users.delete().where(users.c.id_user == id_user))
        return result