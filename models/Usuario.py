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

    # Relación con publicaciones, lugares y viajes (usando cadenas de texto)
    publicaciones = relationship("Publicacion", back_populates="usuario", cascade="all, delete")
    lugares = relationship("Lugar", back_populates="usuario", cascade="all, delete")
    viajes = relationship("Viaje", back_populates="usuario", cascade="all, delete")
    


