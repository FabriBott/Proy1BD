from pydantic import BaseModel
from datetime import datetime

class PublicacionCreate(BaseModel):
    usuarioId: int
    titulo: str
    descripcion: str
    fechaPublicacion: datetime