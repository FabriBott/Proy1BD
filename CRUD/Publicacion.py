from pymongo import MongoClient
from DB.postgres import SessionLocal
from models.Publicacion import Publicacion
from pymongo.collection import Collection
from bson import ObjectId

from models.publicacion_schema import PublicacionCreate

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



################################################################
#--------------------------Mongo---------------------------------



# Función para crear una publicación
def crear_publicacionM(publicacion: PublicacionCreate, db: Collection):
    publicacion_dict = publicacion.dict()
    resultado = db["publicaciones"].insert_one(publicacion_dict)
    return str(resultado.inserted_id)


# Función para obtener todas las publicaciones
def obtener_publicacionesM(db: Collection):
    publicaciones = db["publicaciones"].find()
    # Convertir a lista y cambiar ObjectId a string
    publicaciones_lista = []
    for publicacion in publicaciones:
        publicacion["_id"] = str(publicacion["_id"])  # Convertir ObjectId a string
        publicaciones_lista.append(publicacion)
    return publicaciones_lista


# Función para obtener una publicación por ID
def obtener_publicacion_por_idM(publicacion_id: str, db: Collection):
    publicacion = db["publicaciones"].find_one({"_id": ObjectId(publicacion_id)})
    if publicacion:
        publicacion["_id"] = str(publicacion["_id"])  # Convertir ObjectId a string
    return publicacion



# Función para dar like a una publicación
def dar_likeM(publicacion_id: str, db: Collection):
    resultado = db["publicaciones"].update_one(
        {"_id": ObjectId(publicacion_id)},
        {"$inc": {"likes": 1}}  # Asume que tienes un campo 'likes'
    )
    return resultado.modified_count > 0

# Función para agregar un comentario a una publicación
def agregar_comentarioM(publicacion_id: str, comentario: str, db: Collection):
    resultado = db["publicaciones"].update_one(
        {"_id": ObjectId(publicacion_id)},
        {"$push": {"comentarios": comentario}}  # Agrega el comentario a la lista
    )
    return resultado.modified_count > 0

# Función para agregar una reacción a una publicación
def agregar_reaccionM(publicacion_id: str, reaccion: str, db: Collection):
    resultado = db["publicaciones"].update_one(
        {"_id": ObjectId(publicacion_id)},
        {"$push": {"reacciones": reaccion}}  # Agrega la reacción a la lista
    )
    return resultado.modified_count > 0