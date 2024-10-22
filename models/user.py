from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str

    #Este se musa para autenticar a un usuario