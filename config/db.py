from sqlalchemy import create_engine, MetaData

# Conexión a la BBDD, en este caso MySQL, usando sqlalchemy
#Create_engine necesita la url de la BBDD
#create_engine("mysql+pymysql://user:password@host:port/database")
engine = create_engine("mysql+pymysql://root:root@localhost:3306/microUsers", echo=True)


#mantiene abierta la conexión a la BBDD (a largo plazo es un problema de rendimiento)
conn = engine.connect()


# Creamos la metadata de la BBDD
metadata = MetaData()
