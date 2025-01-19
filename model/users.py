from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import engine, metadata


users = Table(
    "users",
    metadata,
    Column("id_user", Integer, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("email", String(100), nullable=False, unique=True),
    Column("username", String(50), nullable=False, unique=True),
    Column("password", String(255), nullable=False),
    Column("role", String(50)),
)

metadata.create_all(engine)