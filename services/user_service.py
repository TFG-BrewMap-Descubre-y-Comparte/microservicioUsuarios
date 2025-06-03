from sqlalchemy import select
from config.db import engine
from model.users import users
from werkzeug.security import generate_password_hash
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError

# Cargar variables de entorno
load_dotenv(dotenv_path=".env")

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
    
    # Enviar email de bienvenida
    print(f"Llamando a send_registration_email para {data_user['email']}")
    send_registration_email(data_user["email"], data_user["username"])
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

def send_registration_email(to_email: str, username: str):
    """Envía un correo de bienvenida al usuario registrado"""
    from_email = os.getenv("EMAIL_USER")
    from_password = os.getenv("EMAIL_PASSWORD")

    subject = "Welcome to NomadTaste!"
    body = f"""
        Hi {username},

        Thank you for joining NomadTaste — a platform where we blend the joy of specialty coffee with unique thematic routes.

        We're thrilled to have you on board. Get ready to explore, taste, and enjoy an experience like no other.

        See you on the road!
        The NomadTaste Team
        """

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        print(f"Enviando correo a {to_email} desde {from_email}...")
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, msg.as_string())
        print("Correo enviado correctamente")
    except smtplib.SMTPAuthenticationError:
        print("Error de autenticación: verifica tu EMAIL_USER y EMAIL_PASSWORD")
    except Exception as e:
        print("Error al enviar correo:", str(e))
