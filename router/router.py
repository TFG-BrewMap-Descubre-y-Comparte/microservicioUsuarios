from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from schema.user_schema import UserSchema
from config.db import engine
from model.users import users
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
user = APIRouter()

#Esquemas de respuesta
class MessageResponse(BaseModel):
    message: str

class ErrorResponse(BaseModel):
    error: str


#...............................................................
@user.get("/api/v1/users", 
    response_model=list[UserSchema],
    responses={
        200: {"description": "Lista de usuarios", "model": list[UserSchema]},
        500: {"description": "Error al obtener los usuarios", "model": ErrorResponse},
    })
def get_users():
    try:
        with engine.begin() as connection:  # Abre una transacción explícita
            result = connection.execute(select(users))  # Ejecuta la consulta de usuarios
            users_list = [dict(row._mapping) for row in result]  # Convierte las filas a diccionarios

        # Devuelve los usuarios como una lista de diccionarios
        return JSONResponse(content=users_list, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500) 


# ...............................................................


@user.post("/api/v1/insert/user", 
           response_model=MessageResponse,
    responses={
        201: {"description": "Usuario creado correctamente", "model": MessageResponse}, # 201 es el código de estado para una inserción exitosa
        500: {"description": "Error al crear el usuario", "model": ErrorResponse}, # 500 es el código de estado para un error
    },) # 201 es el código de estado para una inserción exitosa
def create_user(data_user: UserSchema):    
    try:
        # Convierte el objeto recibido en un diccionario
        new_user = data_user.dict()
        # Encripta la contraseña, se le pasa la contraseña y el algoritmo con el que se va a encriptar, 30 es la recursividad de codificación, cuanto mas alto mas seguro pero menos eficiente
        new_user["password"] = generate_password_hash(
            new_user["password"], method="pbkdf2:sha256", salt_length=30
        )
        # Elimina el id_user si está presente, ya que es autoincremental
        if "id_user" in new_user:
            del new_user["id_user"]
        print("Datos que se insertarán:", new_user)
        # Abre una transacción explícita
        with engine.begin() as connection:
            # Ejecuta la inserción usando la conexión transaccional
            result = connection.execute(users.insert().values(new_user))
            print("Resultado de la inserción:", result.rowcount)
        # Devuelve un mensaje de éxito
        return JSONResponse(
            status_code=HTTP_201_CREATED,
            content={"message": "Usuario creado correctamente"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )



#...............................................................
@user.put("/api/v1/update/user/{id}")
def update_user(id: int, data_user: UserSchema):
    print(data_user)