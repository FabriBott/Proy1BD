from DB.postgres import SessionLocal
from models import Publicacion

# Función para crear una publicación
def crear_publicacion(usuario_id, titulo, descripcion, fechaPublicacion):
    session = SessionLocal()
    nueva_publicacion = Publicacion(
        usuarioId=usuario_id,
        titulo=titulo,
        descripcion=descripcion,
        fechaPublicacion=fechaPublicacion
    )
    session.add(nueva_publicacion)
    session.commit()
    session.refresh(nueva_publicacion)
    session.close()
    return nueva_publicacion

# Función para obtener una publicación por ID
def obtener_publicacion_por_id(publicacion_id):
    session = SessionLocal()
    publicacion = session.query(Publicacion).filter(Publicacion.identificador == publicacion_id).first()
    session.close()
    return publicacion
