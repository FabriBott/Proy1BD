from pydantic import BaseModel
from datetime import datetime

# Modelo Pydantic para crear un usuario
class UsuarioCreate(BaseModel):
    nombre: str
    apellidos: str
    username: str
    password: str
    fechaRegistro: datetime
