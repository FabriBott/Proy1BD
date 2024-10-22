from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    lastname: str
    firstname: str
    enabled: bool = True
    credentials: list

#Esta clase guarda los datos de Keycloak y de Postgress    