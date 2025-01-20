# microservicio Usuarios
El microservicio de cusuarios gestiona el registro, consulta y Log in de usuarios de la plataforma, almacenando datos como su nombre, email, nick, y rol. Realizado por Alejandro Navarro García. 

# Guía de uso básica: 

pip install -r requirements -> instalar dependencias para el entorno virtual

cd /ruta/del/proyecto

Ejecutar el entorno virtual: 
  -.\venv\Scripts\activate  -> Windows
  - source venv/bin/activate -> Linux

Ejecutar la aplicación: 
  - uvicorn main:app --reload

url/docs -> Swagger
url/api/v1/users -> consula todos los usuarios
url/api/v1/insert/user -> registra un usuario
