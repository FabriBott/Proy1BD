from pydantic import BaseModel

class adminToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str