from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Crear el motor de conexión a PostgreSQL
DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER', 'user')}:{os.getenv('POSTGRES_PASSWORD', 'password')}@{os.getenv('POSTGRES_HOST', 'postgres')}:{os.getenv('POSTGRES_PORT', 5432)}/{os.getenv('POSTGRES_DB', 'redSocial')}"

# Crear la instancia del motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crear la clase base para los modelos
Base = declarative_base()

# Crear una sesión de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_postgres():
    try:
        # Verificar la conexión
        conn = engine.connect()
        print("Conectado exitosamente a PostgreSQL con SQLAlchemy")
        conn.close()
    except Exception as e:
        print(f"Error al conectar a PostgreSQL: {e}")