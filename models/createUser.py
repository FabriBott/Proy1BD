from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    firstname: str
    lastname: str
    enabled: bool = True
    


#Esta clase guarda los datos de Keycloak y de Postgress    