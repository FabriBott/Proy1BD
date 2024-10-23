from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from DB.postgres import Base
from sqlalchemy.orm import relationship

class Publicacion(Base):
    __tablename__ = "Publicaciones"

    identificador = Column(Integer, primary_key=True, autoincrement=True)
    usuarioId = Column(Integer, ForeignKey("Usuarios.identificador", ondelete="CASCADE"))
    titulo = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=False)
    fechaPublicacion = Column(TIMESTAMP, nullable=False)

    # Relación con usuario
    usuario = relationship("Usuario", back_populates="publicaciones")
