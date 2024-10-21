from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from DB.postgres import Base
from sqlalchemy.orm import relationship

class Lugar(Base):
    __tablename__ = "Lugares"

    identificador = Column(Integer, primary_key=True, autoincrement=True)
    usuarioId = Column(Integer, ForeignKey("Usuarios.identificador", ondelete="CASCADE"))
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    ciudad = Column(String(100), nullable=False)
    pais = Column(String(75), nullable=False)
    fechaCreacion = Column(TIMESTAMP, nullable=False)

    # Relación con usuario (cadena de texto para evitar problemas de importación)
    usuario = relationship("Usuario", back_populates="lugares")
    # Relación con viajes
    viajes_lugares = relationship("ViajeLugar", back_populates="lugar")
