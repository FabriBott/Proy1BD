from DB.postgres import SessionLocal
from models.Publicacion import Publicacion

# Función para crear una publicación
def crear_publicacion(usuarioId, titulo, descripcion, fechaPublicacion):
    session = SessionLocal()
    nueva_publicacion = Publicacion(
        usuarioId=usuarioId,
        titulo=titulo,
        descripcion=descripcion,
        fechaPublicacion=fechaPublicacion
    )
    session.add(nueva_publicacion)
    session.commit()
    session.refresh(nueva_publicacion)
    session.close()
    return nueva_publicacion

# Función para obtener todas las publicaciones
def obtener_publicaciones():
    session = SessionLocal()
    try:
        return session.query(Publicacion).all()
    finally:
        session.close()

# Función para obtener una publicación por ID
def obtener_publicacion_por_id(publicacion_id):
    session = SessionLocal()
    try:
        return session.query(Publicacion).filter(Publicacion.identificador == publicacion_id).first()
    finally:
        session.close()
