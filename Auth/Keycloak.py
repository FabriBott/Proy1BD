from keycloak import KeycloakError, KeycloakOpenID, KeycloakAdmin
from fastapi.security import OAuth2PasswordBearer
import requests

from models.adminToken import adminToken
from models.createUser import UserCreate

# Configuración de Keycloak
KEYCLOAK_SERVER_URL = "http://keycloak:8080/auth"
REALM_NAME = "TestApp"
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

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

async def getToken(user, password):
    token = keycloak_openid.token(user, password)
    return token

async def getUserInfo(userToken):
    userinfo = keycloak_openid.userinfo(userToken)
    return userinfo

async def crearUsuario(user: UserCreate, tokenAdmin: adminToken):

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
        "Authorization": f"Bearer {tokenAdmin.access_token}",
        "Content-Type": "application/json"
    }

    # Realizar la solicitud POST para crear el usuario
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 201:
        return {"status": 0, "message": "Usuario creado exitosamente"}
    else:
        return {"status":-1,"status_code":response.status_code, "detail":response.text}
    
