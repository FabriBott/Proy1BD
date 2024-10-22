from models.Lugar import Lugar
from DB.postgres import SessionLocal
from datetime import datetime

# Función para crear un lugar
# Se recibe el ID del usuario que crea el lugar, el nombre, descripción, ciudad y país
def crear_lugar(usuarioId, nombre, descripcion, ciudad, pais):
    session = SessionLocal()
    try:
        nuevo_lugar = Lugar(
            usuarioId=usuarioId,
            nombre=nombre,
            descripcion=descripcion,
            ciudad=ciudad,
            pais=pais,
            fechaCreacion=datetime.now()
        )
        session.add(nuevo_lugar)
        session.commit()
        session.refresh(nuevo_lugar)  
        return nuevo_lugar 
    finally:
        session.close()

# Función para obtener todos los lugares
def obtener_lugares():
    session = SessionLocal()
    try:
        return session.query(Lugar).all()
    finally:
        session.close()

# Función para obtener un lugar por ID
def obtener_lugar_por_id(lugar_id):
    session = SessionLocal()
    try:
        return session.query(Lugar).filter(Lugar.identificador == lugar_id).first()
    finally:
        session.close()