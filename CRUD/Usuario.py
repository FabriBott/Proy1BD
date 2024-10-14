from models import Usuario
from DB.postgres import SessionLocal

from sqlalchemy.orm import Session
from models.Usuario import UsuarioCreate  # Tu modelo Pydantic
from datetime import datetime

from DB.postgres import SessionLocal

# Función para crear un usuario
def crear_usuario(nombre, apellidos, username, password, fechaRegistro):
    session = SessionLocal()
    nuevo_usuario = Usuario(
        nombre=nombre,
        apellidos=apellidos,
        username=username,
        password=password,
        fechaRegistro=fechaRegistro
    )
    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)
    session.close()
    return nuevo_usuario


# Función para obtener un usuario por ID
def obtener_usuario_por_id(usuario_id):
    session = SessionLocal()
    usuario = session.query(Usuario).filter(Usuario.identificador == usuario_id).first()
    session.close()
    return usuario

# Función para eliminar un usuario
def eliminar_usuario(usuario_id):
    session = SessionLocal()
    usuario = session.query(Usuario).filter(Usuario.identificador == usuario_id).first()
    if usuario:
        session.delete(usuario)
        session.commit()
    session.close()
