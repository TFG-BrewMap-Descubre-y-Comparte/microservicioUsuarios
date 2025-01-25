MICROUSERS Guía

	Uvicorn fastAPI 
	
	Ejecutar: 
	python -m venv venv (si no hay venv)

	.\venv\Scripts\activate 

	pip install -r requirements.txt (si no está instalado todo)
	
	uvicorn main:app --reload
	
Utilizamos SQL alchemy para las conexiones a la BBDD

En Config/db.py realizamos la conexión a la BD

MODEL
	En model/users.py creamos el modelo del usuario:
	importamos Tabla y Columna de sqlalchemy y creamos la tabla: 

	users = Table(
		"users",
		metadata,
		Column("id", Integer, primary_key=True),
		Column("name", String(255), nullable=False),
		Column("username", String(255), nullable=False),
		Column("password", String(255), nullable=False),
		Column("role", Integer),
	)

	Y luego llamamos al metadata y le pasamos el engine con create all

SCHEMA
	Importamos de pydantic BASEMODEL
	
	Creamos una clase User(BaseModel):
		Los atributos que queramos que tenga el modelo