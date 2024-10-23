from typing import List
from pydantic import BaseModel
from datetime import datetime

class PublicacionCreate(BaseModel):
    titulo: str
    descripcion: str
    imageLinks: List[str]
    videoLinks: List[str]
    usuarioId: str
    fechaPublicacion: str
    comentarios: List[str]
    reacciones: List[str]


class Comentario(BaseModel):
    usuarioId: str
    texto: str
    fechaComentario: str