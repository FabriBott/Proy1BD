from sqlalchemy import Column, Integer, Date, ForeignKey
from DB.postgres import Base
from sqlalchemy.orm import relationship

class Viaje(Base):
    __tablename__ = "Viajes"

    identificador = Column(Integer, primary_key=True, autoincrement=True)
    usuarioId = Column(Integer, ForeignKey("Usuarios.identificador", ondelete="CASCADE"))
    fechaInicio = Column(Date, nullable=False)
    fechaFinal = Column(Date)

    # Relación con usuario (cadena de texto)
    usuario = relationship("Usuario", back_populates="viajes")
    # Relación con lugares
    viajes_lugares = relationship("ViajeLugar", back_populates="viaje", cascade="all, delete")
