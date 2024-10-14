from sqlalchemy import Column, Integer, String, TIMESTAMP
from DB.postgres import Base
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "Usuarios"

    identificador = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(25), nullable=False)
    apellidos = Column(String(40), nullable=False)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    fechaRegistro = Column(TIMESTAMP, nullable=False)

    # Relación con publicaciones y viajes
    publicaciones = relationship("Publicacion", back_populates="usuario", cascade="all, delete")
    lugares = relationship("Lugar", back_populates="usuario", cascade="all, delete")
    viajes = relationship("Viaje", back_populates="usuario", cascade="all, delete")

from pydantic import BaseModel
from datetime import datetime

# Modelo Pydantic para crear un usuario
class UsuarioCreate(BaseModel):
    nombre: str
    apellidos: str
    username: str
    password: str
    fechaRegistro: datetime
