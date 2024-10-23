from pydantic import BaseModel

class ViajeLugarCreate(BaseModel):
    viajeId: int
    lugaresId: int