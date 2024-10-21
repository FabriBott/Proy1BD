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

from DB import init_databases
from CRUD.Usuario import crear_usuario
from models import *

##Publicacion
from models.publicacion_schema import PublicacionCreate
from models.Publicacion import Publicacion
from CRUD.Publicacion import crear_publicacion, obtener_publicacion_por_id, obtener_publicaciones


##Lugar
from models.lugar_schema import LugarCreate
from CRUD.Lugar import crear_lugar, obtener_lugar_por_id, obtener_lugares
from models.Lugar import Lugar

##Viaje
from models.viaje_schema import ViajeCreate
from CRUD.Viaje import crear_viaje, obtener_viaje_por_id, obtener_viajes
from models.Viaje import Viaje


##ViajeLugar
from models.viaje_lugar_schema import ViajeLugarCreate
from CRUD.ViajeLugar import asociar_viaje_con_lugar, obtener_viaje_lugar_por_id, obtener_viajes_lugares, obtener_viajes_lugares_detallado


from models.Usuario import Usuario  # Importar la clase Usuario, no el módulo
from models.usuario_schema import UsuarioCreate
from models.response import TokenResponse
from models.createUser import UserCreate
from models.user import User
from models.adminToken import adminToken
from models.newUser import NewUser
from keycloak import KeycloakError, KeycloakOpenID, KeycloakAdmin
from fastapi.security import OAuth2PasswordBearer
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de Keycloak
KEYCLOAK_SERVER_URL = "http://keycloak:8080/auth"
REALM_NAME = "TestApp"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

app = FastAPI()

tokenAdministrativo = None

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
# Configuración de Keycloak
keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_SERVER_URL,
    client_id="my-app-client",
    realm_name=REALM_NAME,
    client_secret_key="cliente-secreta"
)

keycloak_admin = KeycloakAdmin(
    server_url="http://keycloak:8080/admin/realms/",
    username=ADMIN_USERNAME,
    password=ADMIN_PASSWORD,
    realm_name="master",
    client_id="admin-cli",
    client_secret_key="cliente-secreta",
    verify=True
)

keycloak_admin.realm_name = "TestApp"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token/", response_model=TokenResponse)
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        token = keycloak_openid.token(username, password)
        return {"access_token": token['access_token'], "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        userinfo = keycloak_openid.userinfo(token)
        if not userinfo:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        return User(username=userinfo["preferred_username"], email=userinfo["email"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.get("/protected/")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hola {current_user.username}, tu acceso ha sido validado."}

# Función para obtener el token administrativo
def get_admin_token() -> adminToken:
    global tokenAdministrativo

    # URL para obtener el token
    url = "http://keycloak:8080/realms/master/protocol/openid-connect/token"
    data = {
        "client_id": "admin-cli",
        "username": "admin",  # Cambiar según sea necesario
        "password": "admin",  # Cambiar según sea necesario
        "grant_type": "password"
    }

    # Realizar la solicitud POST para obtener el token
    r = requests.post(url, data=data)

    # Verificar si la solicitud fue exitosa
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
def create_user(user: NewUser):
    global tokenAdministrativo  # Usar la variable global

    # Verificar si el token administrativo está disponible, si no, llamarlo
    if tokenAdministrativo is None:
        try:
            get_admin_token()  # Llama a la función para obtener el token
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail="Token administrativo no disponible")

    # URL para crear un nuevo usuario
    url = "http://keycloak:8080/admin/realms/TestApp/users"

    # Datos del nuevo usuario
    data = {
        "username": user.username,
        "email": user.email,
        "firstName": user.firstName,
        "lastName": user.lastName,
        "enabled": user.enabled,
        "credentials": [
            {
                "type": "password",
                "value": "password123",  # Cambia esta contraseña según sea necesario
                "temporary": False
            }
        ]
    }

    # Configurar los headers con el token administrativo
    headers = {
        "Authorization": f"Bearer {tokenAdministrativo.access_token}",
        "Content-Type": "application/json"
    }

    # Realizar la solicitud POST para crear el usuario
    response = requests.post(url, json=data, headers=headers)

    # Verificar la respuesta
    if response.status_code == 201:
        return {"message": "Usuario creado exitosamente"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

@app.post("/logout/")
async def logout(token: str = Depends(oauth2_scheme)):
    try:
        logout_url = "http://keycloak:8080/realms/TestApp/protocol/openid-connect/logout"
        headers = {
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(logout_url, headers=headers)

        # Loguear la respuesta para depuración
        logger.info(f"Response from Keycloak: {response.status_code}, {response.text}")

        if response.status_code == 204:  # No Content
            return {"message": "Logout exitoso."}
        else:
            raise HTTPException(status_code=response.status_code, detail="Error al cerrar sesión.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


####################################################################################
#----------------------Endpoints de Publicaciones----------------------#
@app.post("/crear_publicacion/")
async def crear_publicacion_endpoint(publicacion: PublicacionCreate):
    try:
        nueva_publicacion = crear_publicacion(
            usuarioId=publicacion.usuarioId,
            titulo=publicacion.titulo,
            descripcion=publicacion.descripcion,
            fechaPublicacion=publicacion.fechaPublicacion
        )
        return nueva_publicacion
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/publicaciones/")
async def get_publicaciones():
    try:
        publicaciones = obtener_publicaciones()
        return publicaciones
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/publicaciones/{publicacion_id}")
async def get_publicacion(publicacion_id: int):
    try:
        publicacion = obtener_publicacion_por_id(publicacion_id)
        if not publicacion:
            raise HTTPException(status_code=404, detail="Publicación no encontrada")
        return publicacion
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

####################################################################################
#----------------------Endpoints de Lugares----------------------#
@app.post("/crear_lugar/")
async def crear_lugar_endpoint(lugar: LugarCreate):
    try:
        # Crear lugar en PostgreSQL y obtener el ID
        nuevo_lugar = crear_lugar(
            usuarioId=lugar.usuarioId,
            nombre=lugar.nombre,
            descripcion=lugar.descripcion,
            ciudad=lugar.ciudad,
            pais=lugar.pais
        )
        return nuevo_lugar
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/lugares/")
async def get_lugares():
    try:
        lugares = obtener_lugares()
        return lugares
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/lugares/{lugar_id}")
async def get_lugar(lugar_id: int):
    try:
        lugar = obtener_lugar_por_id(lugar_id)
        if not lugar:
            raise HTTPException(status_code=404, detail="Lugar no encontrado")
        return lugar
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

####################################################################################
#----------------------Endpoints de Viajes----------------------#

@app.post("/crear_viaje/")
async def crear_viaje_endpoint(viaje: ViajeCreate):
    try:
        # Crear el viaje en PostgreSQL usando los datos de entrada
        nuevo_viaje = crear_viaje(
            usuarioId=viaje.usuarioId,
            fechaInicio=viaje.fechaInicio,
            fechaFinal=viaje.fechaFinal
        )

        # Retorna el viaje creado como ViajeResponse
        return nuevo_viaje

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/viajes/")
async def get_viajes():
    try:
        viajes = obtener_viajes()
        return viajes
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/viajes/{viaje_id}")
async def get_viaje(viaje_id: int):
    try:
        viaje = obtener_viaje_por_id(viaje_id)
        if not viaje:
            raise HTTPException(status_code=404, detail="Viaje no encontrado")
        return viaje
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

###################################################################################
#----------------------Endpoints de ViajeLugar----------------------#

@app.post("/asociar_viaje_lugar/")
async def asociar_viaje_lugar_endpoint(viajeLugar: ViajeLugarCreate):
    try:
        # Llama a la función para crear la asociación
        asociacion = asociar_viaje_con_lugar(
            viajeId=viajeLugar.viajeId,
            lugaresId=viajeLugar.lugaresId
        )

        # Retorna la asociación creada como ViajeLugarResponse
        return asociacion

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/viajes_lugares/")
async def get_viajes_lugares():
    try:
        viajes_lugares = obtener_viajes_lugares()
        return viajes_lugares
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/viajes_lugares/{viaje_lugar_id}")
async def get_viaje_lugar(viaje_lugar_id: int):
    try:
        viaje_lugar = obtener_viaje_lugar_por_id(viaje_lugar_id)
        if not viaje_lugar:
            raise HTTPException(status_code=404, detail="Asociación Viaje-Lugar no encontrada")
        return viaje_lugar
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/viajes_lugares/detallado/")
async def get_viajes_lugares_detallado():
    try:
        detalles = obtener_viajes_lugares_detallado()
        if not detalles:
            raise HTTPException(status_code=404, detail="No se encontraron asociaciones de Viajes y Lugares")
        return detalles
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
        
##################################################################################

if __name__ == "__main__":
    uvicorn.run(app, port=8000, host="0.0.0.0", reload=True) 
    #Sin reload=True: El servidor no se recarga automáticamente.
