from models.ViajeLugar import ViajeLugar
from DB.postgres import SessionLocal
from sqlalchemy.orm import joinedload
from models.Viaje import Viaje
from models.Lugar import Lugar
from models.ViajeLugar import ViajeLugar

def asociar_viaje_con_lugar(viajeId, lugaresId):
    session = SessionLocal()
    try:
        asociacion = ViajeLugar(
            viajeId=viajeId,
            lugaresId=lugaresId
        )
        session.add(asociacion)
        session.commit()
        return asociacion
    finally:
        session.close()

# Función para obtener todas las asociaciones de viajes con lugares
def obtener_viajes_lugares():
    session = SessionLocal()
    try:
        return session.query(ViajeLugar).all()
    finally:
        session.close()

# Función para obtener una asociación de viaje con lugar por ID
def obtener_viaje_lugar_por_id(viaje_lugar_id):
    session = SessionLocal()
    try:
        return session.query(ViajeLugar).filter(ViajeLugar.identificador == viaje_lugar_id).first()
    finally:
        session.close()

# Función para obtener la información detallada de los viajes con lugares
def obtener_viajes_lugares_detallado():
    session = SessionLocal()
    try:
        # Realiza una consulta para traer la información combinada
        viajes_lugares = session.query(ViajeLugar).options(
            joinedload(ViajeLugar.viaje).joinedload(Viaje.usuario),
            joinedload(ViajeLugar.lugar)
        ).all()
        
        # Crea una lista con la información detallada
        resultados = []
        for vl in viajes_lugares:
            detalle = {
                "viaje_id": vl.viaje.identificador,
                "usuario_id": vl.viaje.usuarioId,
                "usuario_nombre": vl.viaje.usuario.nombre,  # Nombre del usuario que creó el viaje
                "fecha_inicio": vl.viaje.fechaInicio,
                "fecha_final": vl.viaje.fechaFinal,
                "lugar_id": vl.lugar.identificador,
                "lugar_nombre": vl.lugar.nombre,
                "lugar_ciudad": vl.lugar.ciudad,
                "lugar_pais": vl.lugar.pais
            }
            resultados.append(detalle)
        
        return resultados
    finally:
        session.close()