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
from jose import JWTError
import requests
import redis
from pymongo import MongoClient
from contextlib import asynccontextmanager

from DB import init_databases
from CRUD.Usuario import crear_usuario

from models.Usuario import Usuario  
from models.Usuario import UsuarioCreate
from models.response import TokenResponse
from models.createUser import UserCreate
from models.user import User
from models.adminToken import adminToken
from keycloak import KeycloakError, KeycloakOpenID, KeycloakAdmin
from fastapi.security import OAuth2PasswordBearer
import logging


#Todo: remove before deployment
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#Env variables
# PostgreSQL
postgres_host = os.getenv("POSTGRES_HOST")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_name = os.getenv("POSTGRES_NAME")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")

# Redis
redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")

# MongoDB
mongo_host = os.getenv("MONGO_HOST")
mongo_port = os.getenv("MONGO_PORT")
mongo_initdb_root_username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
mongo_initdb_root_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

# Keycloak
keycloak_server_url = os.getenv("KEYCLOAK_SERVER_URL")
keycloak_realm = os.getenv("KEYCLOAK_REALM")
keycloak_client_id = os.getenv("KEYCLOAK_CLIENT_ID")
keycloak_client_secret = os.getenv("KEYCLOAK_CLIENT_SECRET")
keycloack_admin_user = os.getenv("KEYCLOAK_ADMIN_USER")
keycloack_admin_password = os.getenv("KEYCLOAK_ADMIN_PASSWORD")
keycloak_admincli_user = os.getenv("KEYCLOAK_ADMINCLI_USER")


# MongoDB
mongo_host = os.getenv("MONGO_HOST")
mongo_port = os.getenv("MONGO_PORT")
mongo_initdb_root_username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
mongo_initdb_root_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")

# Keycloak
keycloak_server_url = os.getenv("KEYCLOAK_SERVER_URL")
keycloak_realm = os.getenv("KEYCLOAK_REALM")
keycloak_client_id = os.getenv("KEYCLOAK_CLIENT_ID")
keycloak_client_secret = os.getenv("KEYCLOAK_CLIENT_SECRET")
keycloack_admin_user = os.getenv("KEYCLOAK_ADMIN_USER")
keycloack_admin_password = os.getenv("KEYCLOAK_ADMIN_PASSWORD")
keycloak_admincli_user = os.getenv("KEYCLOAK_ADMINCLI_USER")

#Global variables for the app
connections = {}
tokenAdministrativo = None

# -------------------Ciclo de vida de la aplicación-------------------#
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Código que se ejecuta al iniciar la aplicación (startup)
    logger.debug("Entrando al startup")
    global connections
    connections = init_databases()
    
    # Se ejecuta el resto de la aplicación
    yield

    # Código que se ejecuta al cerrar la aplicación (shutdown)
    logger.debug("Cerrando conexiones")
    #Liberar recursos

#Inicializacion del app con el ciclo de vida especificado
app = FastAPI(lifespan=lifespan)


#----------------------Auth server config----------------------#
keycloak_openid = KeycloakOpenID(
    server_url=keycloak_server_url,
    client_id=keycloak_client_id,
    realm_name=keycloak_realm,
    client_secret_key=keycloak_client_secret
)

keycloak_admin = KeycloakAdmin(
    server_url="http://keycloak:8080/admin/realms/",
    username=keycloack_admin_user,
    password=keycloack_admin_password,
    realm_name=keycloak_realm,
    client_id=keycloak_admincli_user,
    client_secret_key=keycloak_client_secret,
    verify=True
)

keycloak_admin.realm_name = keycloak_realm
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.get("/test")
def testDB():
    global connections
    return {"connections": list(connections.keys())}

#Todo, make the code to test the connections and insertions of data into de DB´s
@app.post("/test")
def testDB():
    global connections
    return {"connections": list(connections.keys())}


#----------------------Endpoints----------------------#


'''
Endpoint para obtener un token de usuario, retorna dicho token si las credenciales son correctas
error 401 en caso de que el token no sea valido
'''
@app.post("/token/", response_model=TokenResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(username, password)
        return {"access_token": token['access_token'], "token_type": "bearer"}
    except Exception as e: #Hay que manejar las excepciones de una mejor forma
        raise HTTPException(status_code=401, detail="Invalid credentials")

'''
Endpoint que retorna los datos del usuario basado en un token JWT proporcionado por el 
servicio auth existente
'''
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        userinfo = keycloak_openid.userinfo(token)
        if not userinfo:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        return User(username=userinfo["preferred_username"], email=userinfo["email"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error de sistema")

'''
Funcion interna para solicitar un token administrativo al sistema de auth para realizar las acciones
'''
def get_admin_token() -> adminToken:
    global tokenAdministrativo

    url = "http://keycloak:8080/realms/master/protocol/openid-connect/token"
    data = {
        "client_id": keycloak_admincli_user,
        "username": keycloack_admin_user,
        "password": keycloack_admin_password,
        "grant_type": "password"
    }

    r = requests.post(url, data=data)

    if r.status_code == 200:
        token_info = r.json()
        tokenAdministrativo = adminToken(
            access_token=token_info.get("access_token"),
            refresh_token=token_info.get("refresh_token"),
            token_type=token_info.get("token_type")
        )
        logger.info("Token administrativo obtenido exitosamente.")
        return tokenAdministrativo
    else:
        logger.error(f"Error al obtener el token: {r.status_code} - {r.text}")
        raise HTTPException(status_code=r.status_code, detail="Error al obtener el token")


@app.post("/create_user/")
def create_user(user: UserCreate):
    global tokenAdministrativo  # Usar la variable global

    if tokenAdministrativo is None:
        try:
            get_admin_token()
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail="Token administrativo no disponible")

    url = "http://keycloak:8080/admin/realms/TestApp/users"
    data = {
        "username": user.username,
        "email": user.email,
        "firstName": user.firstname,
        "lastName": user.lastname,
        "enabled": user.enabled,
        "credentials": [
            {
                "type": "password",
                "value": user.password,  # Cambia esta contraseña según sea necesario
                "temporary": False
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {tokenAdministrativo.access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=data, headers=headers)

    #Enviar solicitud a postgres

    # Verificar la respuesta
    if response.status_code == 201:
        return {"message": "Usuario creado exitosamente"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)


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


@app.post("/logout/")
async def logout(token: str = Depends(oauth2_scheme)):
    try:
        logout_url = "http://keycloak:8080/realms/TestApp/protocol/openid-connect/logout"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(logout_url, headers=headers)

        logger.info(f"Response from Keycloak: {response.status_code}, {response.text}")

        if response.status_code == 204:  
            return {"message": "Logout exitoso."}
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al cerrar sesión.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0")