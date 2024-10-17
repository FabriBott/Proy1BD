from pydantic import BaseModel


class NewUser(BaseModel):
    username: str
    email: str
    firstName: str
    lastName: str
    enabled: bool
    credentials: list