import os

# Configuración de Keycloak
from fastapi.security import OAuth2PasswordBearer
from keycloak import KeycloakAdmin, KeycloakOpenID
import requests

from models.adminToken import adminToken
from models.createUser import UserCreate


KEYCLOAK_SERVER_URL = "http://keycloak:8080/auth"
REALM_NAME = os.getenv("KEYCLOAK_REALM")
ADMIN_USERNAME = os.getenv("KEYCLOAK_ADMIN_USER")
ADMIN_PASSWORD = os.getenv("KEYCLOAK_ADMIN_PASSWORD")


keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_SERVER_URL,
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    realm_name=REALM_NAME,
    client_secret_key=os.getenv("KEYCLOAK_CLIENT_SECRET")
)

keycloak_admin = KeycloakAdmin(
    server_url="http://keycloak:8080/admin/realms/",
    username=ADMIN_USERNAME,
    password=ADMIN_PASSWORD,
    realm_name="master",
    client_id=os.getenv("KEYCLOAK_ADMINCLI_USER"),
    client_secret_key=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    verify=True
)

keycloak_admin.realm_name = REALM_NAME
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def crearUsuario(user: UserCreate, tokenAdministrativo: adminToken):
    
    # URL para crear un nuevo usuario
    url = "http://keycloak:8080/admin/realms/TestApp/users"

    # Datos del nuevo usuario
    data = {
        "username": user.username,
        "email": user.email,
        "firstName": user.firstname,
        "lastName": user.lastname,
        "enabled": True,
        "credentials": [
            {
                "type": "password",
                "value": user.password,  # Cambia esta contraseña según sea necesario
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

    return {"status_code":response.status_code, "detail":response.text}