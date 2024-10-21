from sqlalchemy import Column, Integer, ForeignKey
from DB.postgres import Base
from sqlalchemy.orm import relationship

class ViajeLugar(Base):
    __tablename__ = "Viajes_Lugares"

    identificador = Column(Integer, primary_key=True, autoincrement=True)
    viajeId = Column(Integer, ForeignKey("Viajes.identificador", ondelete="CASCADE"))
    lugaresId = Column(Integer, ForeignKey("Lugares.identificador", ondelete="CASCADE"))

    # Relación con viaje y lugar
    viaje = relationship("Viaje", back_populates="viajes_lugares")
    lugar = relationship("Lugar", back_populates="viajes_lugares")
