import json
import os
import shutil
from typing import Optional
import asyncpg
from http.client import HTTPException
from fastapi import FastAPI, Form
import uvicorn
from fastapi import FastAPI, HTTPException, UploadFile, File, status, Form, Depends
from pydantic import BaseModel

import redis

from DB import init_databases
from CRUD.Usuario import crear_usuario
from models import *

from models.Usuario import Usuario  # Importar la clase Usuario, no el módulo
from models.Usuario import UsuarioCreate
from models.response import TokenResponse

from keycloak import KeycloakOpenID, KeycloakAdmin
from fastapi.security import OAuth2PasswordBearer



app = FastAPI()


@app.on_event("startup")
async def startup():
    init_databases()



@app.post("/usuarios/")
async def crear_usuario_endpoint(usuario: UsuarioCreate):
    nuevo_usuario = crear_usuario(
        nombre=usuario.nombre,
        apellidos=usuario.apellidos,
        username=usuario.username,
        password=usuario.password,
        fechaRegistro=usuario.fechaRegistro
    )
    return nuevo_usuario

#----------------------Auth server config----------------------#
keycloak_openid = KeycloakOpenID(
    server_url="http://keycloak:8080/auth",
    client_id="my-app-client",
    realm_name="TestApp",
    client_secret_key="client-secreta"
)

keycloak_admin = KeycloakAdmin(
    server_url="http://keycloak:8080/auth/",
    username="admin",
    password="AdminPassword",
    realm_name="master",  # Realm principal donde resides el usuario admin
    client_id="admin-cli",  # Este es el cliente de administración predeterminado
    verify=True
)

keycloak_admin.realm_name = "TestApp"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependencia para verificar el token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        
        # Obtener la clave pública de Keycloak
        public_key = keycloak_openid.public_key()
        
        # Decodificar el token
        decoded_token = keycloak_openid.decode_token(token, public_key)

        # Verificar la validez del token
        if 'exp' not in decoded_token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return decoded_token


@app.post("/token/", response_model=TokenResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        # Obtener token de Keycloak
        token = keycloak_openid.token(username, password)
        return {"access_token": token['access_token'], "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")


#----------------------Postgres server config----------------------#



#----------------------Redis server config----------------------#

#----------------------Mongo server config----------------------#

#----------------------Endpoints server config----------------------#

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")