from models.Viaje import Viaje
from DB.postgres import SessionLocal

def crear_viaje(usuarioId, fechaInicio, fechaFinal):
    session = SessionLocal()
    try:
        nuevo_viaje = Viaje(
            usuarioId=usuarioId,
            fechaInicio=fechaInicio,
            fechaFinal=fechaFinal
        )
        session.add(nuevo_viaje)
        session.commit()
        session.refresh(nuevo_viaje)  # Obtener el ID generado
        return nuevo_viaje
    finally:
        session.close()

def obtener_viajes():
    session = SessionLocal()
    try:
        return session.query(Viaje).all()
    finally:
        session.close()

def obtener_viaje_por_id(viaje_id):
    session = SessionLocal()
    try:
        return session.query(Viaje).filter(Viaje.identificador == viaje_id).first()
    finally:
        session.close()