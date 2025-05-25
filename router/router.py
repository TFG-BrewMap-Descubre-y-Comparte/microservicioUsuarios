from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from services.user_service import get_all_users, get_user_by_id, create_user, update_user, delete_user
from services.auth_service import get_current_user, authenticate_user, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from schema.user_schema import UserSchema, DataUser, UserResponse, ErrorResponse, MessageResponse
from starlette.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR

user_router = APIRouter()

# ............................................................... GET ALL
@user_router.get("/api/v1/users", 
    response_model=list[UserResponse],  # Usamos UserResponse en lugar de UserSchema
    responses={200: {"description": "Lista de usuarios", "model": list[UserResponse]}, 500: {"description": "Error al obtener los usuarios", "model": ErrorResponse}})
def get_users(current_user: dict = Depends(get_current_user)):  # Dependencia para verificar token
    try:
        users_list = get_all_users()
        # Convertir los usuarios a UserResponse para eliminar contraseñas
        users_response = [UserResponse(**user) for user in users_list]
        return JSONResponse(content=users_response, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# ............................................................... GET ONE
@user_router.get("/api/v1/user/{id_user}", 
    response_model=UserResponse,  
    responses={200: {"description": "Usuario encontrado", "model": UserResponse}, 404: {"description": "Usuario no encontrado", "model": ErrorResponse}})
def get_user(id_user: str, current_user: dict = Depends(get_current_user)):  # Dependencia para verificar token
    try:
        # el usuario existe
        user_data = get_user_by_id(id_user)
        if user_data is None:
            return JSONResponse(content={"error": "Usuario no encontrado"}, status_code=404)
        
        # UserResponse
        user_response = UserResponse(**user_data)
        return JSONResponse(content=user_response.dict(), status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# ............................................................... INSERT
@user_router.post("/api/v1/insert/user", 
    response_model=MessageResponse, 
    responses={201: {"description": "Usuario creado correctamente", "model": MessageResponse}, 500: {"description": "Error al crear el usuario", "model": ErrorResponse}})
def create_user_route(data_user: UserSchema):  
    try:
        existing_user = get_user_by_id(data_user.username)
        if existing_user:
            return JSONResponse(content={"error": "El usuario ya existe"}, status_code=400)

        new_user = data_user.dict()
        if "id_user" in new_user:
            del new_user["id_user"]

        # Crea el usuario (y se hashea dentro de esa función)
        create_user(new_user)

        return JSONResponse(status_code=HTTP_201_CREATED, content={"message": "Usuario creado correctamente"})
    except Exception as e:
        return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})
# ............................................................... LOGIN
@user_router.post("/api/v1/login/user", response_model=UserResponse)
def login_user(data_user: DataUser):
    try:
        user_data = authenticate_user(data_user.username, data_user.password)
        if not user_data:
            return JSONResponse(content={"error": "Usuario o contraseña incorrectos"}, status_code=401)
        
        access_token = create_access_token(data={"sub": user_data["username"], "id_user": user_data["id_user"]})
        
        user_response = UserResponse(
            id_user=user_data["id_user"],
            username=user_data["username"],
            name=user_data["name"],
            email=user_data["email"],
            role=user_data["role"]
        )
        
        return JSONResponse(content={"user": user_response.dict(), "access_token": access_token}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# ............................................................... UPDATE
@user_router.put("/api/v1/update/user/{id}", 
    response_model=UserResponse,  # Cambiado a UserResponse
    responses={200: {"description": "Usuario actualizado", "model": UserResponse}, 404: {"description": "Usuario no encontrado", "model": ErrorResponse}, 500: {"description": "Error al actualizar el usuario", "model": ErrorResponse}})
def update_user_route(id: int, data_user: UserSchema, current_user: dict = Depends(get_current_user)):  # Dependencia para verificar token
    try:
        # Comprobación si el usuario existe
        existing_user = get_user_by_id(id)
        if existing_user is None:
            return JSONResponse(content={"error": "Usuario no encontrado"}, status_code=404)

        # Cifra la contraseña antes de actualizarla
        hashed_password = generate_password_hash(data_user.password, method="pbkdf2:sha256", salt_length=30)

        # Actualiza el usuario
        update_user(id, {
            "name": data_user.name,
            "email": data_user.email,
            "username": data_user.username,
            "password": hashed_password,
            "role": data_user.role
        })
        
        # Devuelve el usuario actualizado sin la contraseña
        updated_user = get_user_by_id(id)
        user_response = UserResponse(**updated_user)
        return JSONResponse(content=user_response.dict(), status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

# ............................................................... DELETE
@user_router.delete("/api/v1/delete/user/{id}", 
    responses={200: {"description": "Usuario eliminado exitosamente"}, 404: {"description": "Usuario no encontrado", "model": ErrorResponse}, 500: {"description": "Error al eliminar el usuario", "model": ErrorResponse}})
def delete_user_route(id: int, current_user: dict = Depends(get_current_user)):  # Dependencia para verificar token
    try:
        # Comprobación si el usuario existe
        existing_user = get_user_by_id(id)
        if existing_user is None:
            return JSONResponse(content={"error": "Usuario no encontrado"}, status_code=404)

        # Elimina el usuario
        delete_user(id)
        return JSONResponse(content={"message": "Usuario eliminado exitosamente"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@user_router.get("/api/internal/user/{id_user}", 
    response_model=UserResponse,
    responses={
        200: {"description": "Usuario encontrado", "model": UserResponse},
        404: {"description": "Usuario no encontrado", "model": ErrorResponse}
    })
def get_user_internal(id_user: str):
    """
    Ruta interna que devuelve datos de un usuario sin requerir autenticación.
    Útil para llamadas internas entre microservicios.
    """
    try:
        user_data = get_user_by_id(id_user)
        if user_data is None:
            return JSONResponse(content={"error": "Usuario no encontrado"}, status_code=404)

        return JSONResponse(content=UserResponse(**user_data).dict(), status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
