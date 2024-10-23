from pydantic import BaseModel
from datetime import date

# BaseModel para representar los datos de un viaje
class ViajeCreate(BaseModel):
    usuarioId: int
    fechaInicio: date
    fechaFinal: date
