from pydantic import BaseModel
from datetime import datetime

class LugarCreate (BaseModel):
    usuarioId: int
    nombre: str
    descripcion: str
    ciudad: str
    pais: str