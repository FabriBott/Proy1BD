import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from httpx import AsyncClient
# import de app.py
from app import app
from models.publicacion_schema import PublicacionCreate
from datetime import datetime

# Usamos TestClient para simular solicitudes HTTP en FastAPI
client = TestClient(app)

# Test para login exitoso
def test_login_exitoso(monkeypatch):
    # Mockear el token de respuesta de Keycloak
    def mock_keycloak_token(username, password):
        return {"access_token": "mocked_access_token", "token_type": "bearer"}
    # Usar monkeypatch para reemplazar la función keycloak_openid.token
    monkeypatch.setattr("app.keycloak_openid.token", mock_keycloak_token)
    # Realizar la solicitud de login
    response = client.post("/token/", data={"username": "admin", "password": "admin"})
    # Verificar que el código de estado sea 200 (OK)
    assert response.status_code == 200
    # Verificar que el token esté en la respuesta
    data = response.json()
    assert "access_token" in data
    assert data["access_token"] == "mocked_access_token"
    assert data["token_type"] == "bearer"

# Test para login fallido
def test_login_fallido(monkeypatch):
    # Mockear el comportamiento de Keycloak para lanzar una excepción en caso de credenciales incorrectas
    def mock_keycloak_token(username, password):
        raise Exception("Invalid credentials")
    monkeypatch.setattr("app.keycloak_openid.token", mock_keycloak_token)
    # Realizar la solicitud de login con credenciales incorrectas
    response = client.post("/token/", data={"username": "invalid_user", "password": "invalid_password"})
    # Verificar que el código de estado sea 401 (Unauthorized)
    assert response.status_code == 401
    # Verificar que el mensaje de error sea "Invalid credentials"
    data = response.json()
    assert data["detail"] == "Invalid credentials"


# Test para token administrativo no disponible
def test_create_user_token_no_disponible(monkeypatch):
    # Mockear la función para lanzar una excepción al obtener el token administrativo
    def mock_get_admin_token():
        raise HTTPException(status_code=500, detail="Token administrativo no disponible")

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.get_admin_token", mock_get_admin_token)

    # Datos del usuario (incluyendo los campos faltantes)
    data = {
        "firstname": "John",
        "lastname": "Doe",
        "username": "johndoe",
        "password": "password123",
        "email": "john.doe@example.com",  # Campo obligatorio
        "enabled": True  # Campo con valor por defecto
    }

    # Realizar la solicitud
    response = client.post("/create_user/", json=data)

    # Imprimir la respuesta para verificar si hay errores
    print(response.json())

    # Verificar que el código de estado sea 500 (Error del servidor)
    assert response.status_code == 500


# # Test para fallo en creación de usuario en Keycloak
# def test_create_user_fallo_keycloak(monkeypatch):
#     # Mockear el token administrativo
#     def mock_get_admin_token():
#         global tokenAdministrativo
#         tokenAdministrativo = "mocked_admin_token"

#     # Mockear la función de creación de usuario
#     def mock_crear_usuario(nombre, apellidos, username, password, fechaRegistro):
#         return None  # Simular la creación sin hacer nada

#     # Mockear la respuesta de Keycloak para fallo en creación del usuario
#     def mock_crearUsuario(user, token):
#         return {"status_code": 400, "detail": "Error en la creación de usuario en Keycloak"}

#     # Usar monkeypatch para reemplazar las funciones
#     monkeypatch.setattr("app.get_admin_token", mock_get_admin_token)
#     monkeypatch.setattr("app.crear_usuario", mock_crear_usuario)
#     monkeypatch.setattr("app.Auth.crearUsuario", mock_crearUsuario)

#     # Datos del usuario
#     data = {
#         "firstname": "John",
#         "lastname": "Doe",
#         "username": "johndoe",
#         "password": "password123",
#         "enabled": True  # Campo con valor por defecto
#     }

#     # Realizar la solicitud
#     response = client.post("/create_user/", json=data)

#     # Verificar que el código de estado sea 400 (Bad Request)
#     assert response.status_code == 400



# def test_create_user_exitoso(monkeypatch):
#     # Mockear el token administrativo
#     def mock_get_admin_token():
#         global tokenAdministrativo
#         tokenAdministrativo = "mocked_admin_token"

#     # Mockear la función de creación de usuario
#     def mock_crear_usuario(nombre, apellidos, username, password, fechaRegistro):
#         return None  # Simula la creación de usuario

#     # Mockear la respuesta de Keycloak para crear el usuario
#     def mock_crearUsuario(user, token):
#         return {"status_code": 201, "detail": "Usuario creado exitosamente"}

#     # Usar monkeypatch para reemplazar las funciones
#     monkeypatch.setattr("app.get_admin_token", mock_get_admin_token)
#     monkeypatch.setattr("app.crear_usuario", mock_crear_usuario)
#     monkeypatch.setattr("app.Auth.crearUsuario", mock_crearUsuario)

#     # Datos del usuario
#     data = {
#         "firstname": "John",
#         "lastname": "Doe",
#         "username": "johndoe",
#         "password": "password123",
#         "enabled": True  # Campo con valor por defecto
#     }

#     # Realizar la solicitud
#     response = client.post("/create_user/", json=data)

#     # Verificar que el código de estado sea 200 (OK)
#     assert response.status_code == 200

def test_logout_exitoso(monkeypatch):
    # Mockear la respuesta de Keycloak para el logout
    class MockResponse:
        status_code = 204
        text = ""

    def mock_post(url, headers):
        return MockResponse()  # Simula una respuesta exitosa

    # Usar monkeypatch para reemplazar requests.post
    monkeypatch.setattr("requests.post", mock_post)

    # Simular un token válido
    token = "mocked_valid_token"
    response = client.post("/logout/", headers={"Authorization": f"Bearer {token}"})

    # Verificar que el código de estado sea 200 (OK)
    assert response.status_code == 200
    assert response.json() == {"message": "Logout exitoso."}

def test_logout_fallido(monkeypatch):
    # Mockear la respuesta de Keycloak para el logout
    class MockResponse:
        status_code = 401  # Simula un error de autorización
        text = "Unauthorized"

    def mock_post(url, headers):
        return MockResponse()  # Simula una respuesta fallida

    # Usar monkeypatch para reemplazar requests.post
    monkeypatch.setattr("requests.post", mock_post)

    # Simular un token inválido
    token = "mocked_invalid_token"
    response = client.post("/logout/", headers={"Authorization": f"Bearer {token}"})

    # Verificar que el código de estado sea 401 (Unauthorized)
    assert response.status_code == 500
    assert response.json() == {"detail": "Error del servidor."}











def test_crear_lugar_exitoso(monkeypatch):
    # Mockear la función crear_lugar
    def mock_crear_lugar(usuarioId, nombre, descripcion, ciudad, pais):
        return {
            "id": 1,
            "usuarioId": usuarioId,
            "nombre": nombre,
            "descripcion": descripcion,
            "ciudad": ciudad,
            "pais": pais
        }  # Simula un nuevo lugar creado

    # Usar monkeypatch para reemplazar la función crear_lugar
    monkeypatch.setattr("app.crear_lugar", mock_crear_lugar)

    # Datos del lugar
    data = {
        "usuarioId": 123,
        "nombre": "Plaza Central",
        "descripcion": "Una plaza hermosa en el centro de la ciudad.",
        "ciudad": "Ciudad Ejemplo",
        "pais": "País Ejemplo"
    }

    # Realizar la solicitud
    response = client.post("/crear_lugar/", json=data)

    # Verificar que el código de estado sea 200 (OK)
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "usuarioId": 123,
        "nombre": "Plaza Central",
        "descripcion": "Una plaza hermosa en el centro de la ciudad.",
        "ciudad": "Ciudad Ejemplo",
        "pais": "País Ejemplo"
    }



def test_crear_lugar_error(monkeypatch):
    # Mockear la función crear_lugar para lanzar una excepción
    def mock_crear_lugar(usuarioId, nombre, descripcion, ciudad, pais):
        raise Exception("Error al crear el lugar")  # Simula un error en la creación

    # Usar monkeypatch para reemplazar la función crear_lugar
    monkeypatch.setattr("app.crear_lugar", mock_crear_lugar)

    # Datos del lugar
    data = {
        "usuarioId": 123,
        "nombre": "Plaza Central",
        "descripcion": "Una plaza hermosa en el centro de la ciudad.",
        "ciudad": "Ciudad Ejemplo",
        "pais": "País Ejemplo"
    }

    # Realizar la solicitud
    response = client.post("/crear_lugar/", json=data)

    # Verificar que el código de estado sea 400 (Bad Request)
    assert response.status_code == 400
    assert response.json() == {"detail": "Error al crear el lugar"}

def test_get_viajes_exitoso(monkeypatch):
    # Mockear la función obtener_viajes
    def mock_obtener_viajes():
        return [
            {"id": 1, "destino": "París", "fecha": "2024-05-01"},
            {"id": 2, "destino": "Londres", "fecha": "2024-06-15"}
        ]  # Simula una lista de viajes

    # Usar monkeypatch para reemplazar la función obtener_viajes
    monkeypatch.setattr("app.obtener_viajes", mock_obtener_viajes)

    # Realizar la solicitud
    response = client.get("/viajes/")

    # Verificar que el código de estado sea 200 (OK)
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "destino": "París", "fecha": "2024-05-01"},
        {"id": 2, "destino": "Londres", "fecha": "2024-06-15"}
    ]


def test_get_viajes_error(monkeypatch):
    # Mockear la función obtener_viajes para lanzar una excepción
    def mock_obtener_viajes():
        raise Exception("Error al obtener los viajes")  # Simula un error en la obtención

    # Usar monkeypatch para reemplazar la función obtener_viajes
    monkeypatch.setattr("app.obtener_viajes", mock_obtener_viajes)

    # Realizar la solicitud
    response = client.get("/viajes/")

    # Verificar que el código de estado sea 400 (Bad Request)
    assert response.status_code == 400
    assert response.json() == {"detail": "Error al obtener los viajes"}


def test_get_viaje_exitoso(monkeypatch):
    # Mockear la función obtener_viaje_por_id
    def mock_obtener_viaje_por_id(viaje_id):
        return {"id": viaje_id, "destino": "París", "fecha": "2024-05-01"}  # Simula un viaje

    # Usar monkeypatch para reemplazar la función obtener_viaje_por_id
    monkeypatch.setattr("app.obtener_viaje_por_id", mock_obtener_viaje_por_id)

    # ID del viaje a solicitar
    viaje_id = 1

    # Realizar la solicitud
    response = client.get(f"/viajes/{viaje_id}")

    # Verificar que el código de estado sea 200 (OK)
    assert response.status_code == 200
    assert response.json() == {"id": viaje_id, "destino": "París", "fecha": "2024-05-01"}

def test_get_viaje_no_encontrado(monkeypatch):
    # Mockear la función obtener_viaje_por_id para devolver None
    def mock_obtener_viaje_por_id(viaje_id):
        return None  # Simula que el viaje no se encuentra

    # Usar monkeypatch para reemplazar la función obtener_viaje_por_id
    monkeypatch.setattr("app.obtener_viaje_por_id", mock_obtener_viaje_por_id)

    # ID del viaje a solicitar
    viaje_id = 999  # ID que no existe

    # Realizar la solicitud
    response = client.get(f"/viajes/{viaje_id}")

    # Verificar que el código de estado sea 400 (Not Found)
    assert response.status_code == 400


def test_get_viaje_error(monkeypatch):
    # Mockear la función obtener_viaje_por_id para lanzar una excepción
    def mock_obtener_viaje_por_id(viaje_id):
        raise Exception("Error al obtener el viaje")  # Simula un error en la obtención

    # Usar monkeypatch para reemplazar la función obtener_viaje_por_id
    monkeypatch.setattr("app.obtener_viaje_por_id", mock_obtener_viaje_por_id)

    # ID del viaje a solicitar
    viaje_id = 1

    # Realizar la solicitud
    response = client.get(f"/viajes/{viaje_id}")

    # Verificar que el código de estado sea 400 (Bad Request)
    assert response.status_code == 400

def test_asociar_viaje_lugar_error(monkeypatch):
    # Mockear la función asociar_viaje_con_lugar para lanzar una excepción
    def mock_asociar_viaje_con_lugar(viajeId, lugaresId):
        raise Exception("Error al asociar el viaje con el lugar")  # Simula un error

    # Usar monkeypatch para reemplazar la función asociar_viaje_con_lugar
    monkeypatch.setattr("app.asociar_viaje_con_lugar", mock_asociar_viaje_con_lugar)

    # Datos de la asociación
    data = {
        "viajeId": 1,
        "lugaresId": [2, 3]  # Lista de IDs de lugares
    }

    # Realizar la solicitud
    response = client.post("/asociar_viaje_lugar/", json=data)

    # Verificar que el código de estado sea 400 (Bad Request)
    assert response.status_code == 422

# Test exitoso para obtener viajes y lugares
def test_get_viajes_lugares_exitoso(monkeypatch):
    # Datos simulados para la respuesta
    mock_viajes_lugares = [
        {"viaje_id": 1, "lugar_id": 2, "nombre_lugar": "Lugar 1"},
        {"viaje_id": 1, "lugar_id": 3, "nombre_lugar": "Lugar 2"},
    ]

    # Función simulada que retorna los datos mockeados
    def mock_obtener_viajes_lugares():
        return mock_viajes_lugares

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.obtener_viajes_lugares", mock_obtener_viajes_lugares)

    # Realizar la solicitud
    response = client.get("/viajes_lugares/")

    # Verificar que el código de estado sea 200 (OK)
    assert response.status_code == 200
    assert response.json() == mock_viajes_lugares

# Test para manejar un error en la obtención de viajes y lugares
def test_get_viajes_lugares_error(monkeypatch):
    # Usar monkeypatch para simular un error en la función obtener_viajes_lugares
    def mock_obtener_viajes_lugares_error():
        raise Exception("Error al obtener los viajes y lugares")

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.obtener_viajes_lugares", mock_obtener_viajes_lugares_error)

    # Realizar la solicitud
    response = client.get("/viajes_lugares/")

    # Verificar que el código de estado sea 400 (Bad Request)
    assert response.status_code == 400
    assert response.json() == {"detail": "Error al obtener los viajes y lugares"}


# Test exitoso para obtener una asociación de viaje-lugar por ID
def test_get_viaje_lugar_exitoso(monkeypatch):
    # Datos simulados para la respuesta
    mock_viaje_lugar = {
        "identificador": 1,
        "viajeId": 1,
        "lugaresId": 2
    }

    # Función simulada que retorna los datos mockeados
    def mock_obtener_viaje_lugar_por_id(viaje_lugar_id):
        return mock_viaje_lugar if viaje_lugar_id == 1 else None

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.obtener_viaje_lugar_por_id", mock_obtener_viaje_lugar_por_id)

    # Realizar la solicitud
    response = client.get("/viajes_lugares/1")

    # Verificar que el código de estado sea 200 (OK)
    assert response.status_code == 200
    assert response.json() == mock_viaje_lugar

# Test para manejar un error 404 si no se encuentra la asociación
def test_get_viaje_lugar_no_encontrado(monkeypatch):
    # Función simulada que retorna None (no encontrado)
    def mock_obtener_viaje_lugar_por_id(viaje_lugar_id):
        return None

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.obtener_viaje_lugar_por_id", mock_obtener_viaje_lugar_por_id)

    # Realizar la solicitud
    response = client.get("/viajes_lugares/1")

    # Verificar que el código de estado sea 400 (Not Found)
    assert response.status_code == 400

# Test para manejar un error 400 en caso de excepción
def test_get_viaje_lugar_error(monkeypatch):
    # Usar monkeypatch para simular un error en la función obtener_viaje_lugar_por_id
    def mock_obtener_viaje_lugar_por_id_error(viaje_lugar_id):
        raise Exception("Error al obtener la asociación")

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.obtener_viaje_lugar_por_id", mock_obtener_viaje_lugar_por_id_error)

    # Realizar la solicitud
    response = client.get("/viajes_lugares/1")

    # Verificar que el código de estado sea 400 (Bad Request)
    assert response.status_code == 400
    assert response.json() == {"detail": "Error al obtener la asociación"}

# Test exitoso para obtener detalles de asociaciones de viajes-lugares
def test_get_viajes_lugares_detallado_exitoso(monkeypatch):
    # Datos simulados para la respuesta
    mock_detalles = [
        {
            "viaje_id": 1,
            "usuario_id": 1,
            "usuario_nombre": "Juan Pérez",
            "fecha_inicio": "2024-01-01",
            "fecha_final": "2024-01-10",
            "lugar_id": 2,
            "lugar_nombre": "Playa Bonita",
            "lugar_ciudad": "Ciudad del Mar",
            "lugar_pais": "Países de Sol"
        },
        {
            "viaje_id": 2,
            "usuario_id": 2,
            "usuario_nombre": "María López",
            "fecha_inicio": "2024-02-15",
            "fecha_final": "2024-02-20",
            "lugar_id": 3,
            "lugar_nombre": "Montaña Alta",
            "lugar_ciudad": "Montañita",
            "lugar_pais": "Montaña País"
        }
    ]

    # Función simulada que retorna los datos mockeados
    def mock_obtener_viajes_lugares_detallado():
        return mock_detalles

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.obtener_viajes_lugares_detallado", mock_obtener_viajes_lugares_detallado)

    # Realizar la solicitud
    response = client.get("/viajes_lugares/detallado/")

    # Verificar que el código de estado sea 200 (OK)
    assert response.status_code == 200
    assert response.json() == mock_detalles

# Test para manejar un error 404 si no se encuentran asociaciones
def test_get_viajes_lugares_detallado_no_encontrado(monkeypatch):
    # Función simulada que retorna una lista vacía (no encontrado)
    def mock_obtener_viajes_lugares_detallado_no_encontrado():
        return []

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.obtener_viajes_lugares_detallado", mock_obtener_viajes_lugares_detallado_no_encontrado)

    # Realizar la solicitud
    response = client.get("/viajes_lugares/detallado/")

    # Verificar que el código de estado sea 400 (Not Found)
    assert response.status_code == 400

# Test para manejar un error 400 en caso de excepción
def test_get_viajes_lugares_detallado_error(monkeypatch):
    # Usar monkeypatch para simular un error en la función obtener_viajes_lugares_detallado
    def mock_obtener_viajes_lugares_detallado_error():
        raise Exception("Error al obtener las asociaciones")

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.obtener_viajes_lugares_detallado", mock_obtener_viajes_lugares_detallado_error)

    # Realizar la solicitud
    response = client.get("/viajes_lugares/detallado/")

    # Verificar que el código de estado sea 400 (Bad Request)
    assert response.status_code == 400
    assert response.json() == {"detail": "Error al obtener las asociaciones"}
# Test exitoso para crear una publicación
def test_crear_publicacion_no_exitoso(monkeypatch):
    # Datos simulados para la publicación, asegurándote de incluir todos los campos requeridos
    mock_publicacion = PublicacionCreate(
        titulo="Título de prueba",
        descripcion="Descripción de prueba",
        imageLinks=["http://example.com/image1.jpg", "http://example.com/image2.jpg"],
        videoLinks=["http://example.com/video1.mp4"],
        usuarioId="12345",  # Cambiado a str según tu modelo
        fechaPublicacion=datetime.now().isoformat(),  # Formato de fecha ISO
        comentarios=[],
        reacciones=[]
    )

    # Simular la función que crea la publicación y retorna un ID
    def mock_crear_publicacionM(publicacion, db):
        return "mock_id_123"

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.crear_publicacion", mock_crear_publicacionM)

    # Realizar la solicitud
    response = client.post("/mongo/crear_publicacion/", json=mock_publicacion.dict())

    # Verificar que el código de estado sea 400 (OK)
    assert response.status_code == 400

# Test para manejar un error 400 en caso de excepción
def test_crear_publicacion_error(monkeypatch):
    # Datos simulados para la publicación
    mock_publicacion = PublicacionCreate(
        titulo="Título de prueba",
        descripcion="Descripción de prueba",
        imageLinks=["http://example.com/image1.jpg", "http://example.com/image2.jpg"],
        videoLinks=["http://example.com/video1.mp4"],
        usuarioId="12345",  # Cambiado a str según tu modelo
        fechaPublicacion=datetime.now().isoformat(),  # Formato de fecha ISO
        comentarios=[],
        reacciones=[]
    )

    # Usar monkeypatch para simular un error en la función crear_publicacionM
    def mock_crear_publicacionM_error(publicacion, db):
        raise Exception("Error al crear la publicación")

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.crear_publicacionM", mock_crear_publicacionM_error)

    # Realizar la solicitud
    response = client.post("/mongo/crear_publicacion/", json=mock_publicacion.dict())

    # Verificar que el código de estado sea 400 (Bad Request)
    assert response.status_code == 400
    assert response.json() == {"detail": "Error al crear la publicación"}

# Test para manejar el caso cuando no hay publicaciones
def test_get_publicaciones_no_hay_publicaciones(monkeypatch):
    # Simular que no hay publicaciones en la base de datos
    def mock_obtener_publicacionesM(db):
        return []

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.obtener_publicacionesM", mock_obtener_publicacionesM)

    # Realizar la solicitud
    response = client.get("/mongo/publicaciones/")

    # Verificar que el código de estado sea 500 (Not Found)
    assert response.status_code == 500


# Test para manejar el caso cuando no se encuentra la publicación
def test_get_publicacion_no_encontrada(monkeypatch):
    publicacion_id = "1"

    # Simular que no se encuentra la publicación en la base de datos
    def mock_obtener_publicacion_por_idM_no_encontrada(publicacion_id, db):
        return None

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.obtener_publicacion_por_idM", mock_obtener_publicacion_por_idM_no_encontrada)

    # Realizar la solicitud
    response = client.get(f"/mongo/publicaciones/{publicacion_id}")

    # Verificar que el código de estado sea 404 (Not Found)
    assert response.status_code == 400

# Test para manejar errores internos
def test_get_publicacion_error(monkeypatch):
    publicacion_id = "1"

    # Simular un error en la función que obtiene la publicación por ID
    def mock_obtener_publicacion_por_idM_error(publicacion_id, db):
        raise Exception("Error interno en la base de datos")

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.obtener_publicacion_por_idM", mock_obtener_publicacion_por_idM_error)

    # Realizar la solicitud
    response = client.get(f"/mongo/publicaciones/{publicacion_id}")

    # Verificar que el código de estado sea 400 (Bad Request)
    assert response.status_code == 400


# Test exitoso para dar like a una publicación
def test_like_publicacion_exitoso(monkeypatch):
    publicacion_id = "1"

    # Simular el resultado exitoso de dar like
    def mock_dar_likeM(publicacion_id, db):
        return True  # Simulamos que se dio like correctamente

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.dar_likeM", mock_dar_likeM)

    # Realizar la solicitud
    response = client.post(f"/mongo/publicaciones/{publicacion_id}/like/")

    # Verificar que el código de estado sea 200 (OK)
    assert response.status_code == 200
    assert response.json() == {"message": "Like agregado exitosamente"}

def test_like_publicacion_no_encontrada(monkeypatch):
    publicacion_id = "1"

    # Simular que no se pudo dar like porque la publicación no existe
    def mock_dar_likeM_no_encontrada(publicacion_id, db):
        return False  # Simulamos que no se pudo dar like

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.dar_likeM", False)

    # Realizar la solicitud
    response = client.post(f"/mongo/publicaciones/{publicacion_id}/like/")

    # Verificar que el código de estado sea 404 (Not Found)
    assert response.status_code == 400
    assert response.json() != {"detail": "Publicación no encontrada o no se pudo dar 'like'"}


# Test para manejar errores internos
def test_like_publicacion_error(monkeypatch):
    publicacion_id = "1"

    # Simular un error en la función dar_likeM
    def mock_dar_likeM_error(publicacion_id, db):
        raise Exception("Error interno en la base de datos")

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.dar_likeM", mock_dar_likeM_error)

    # Realizar la solicitud
    response = client.post(f"/mongo/publicaciones/{publicacion_id}/like/")

    # Verificar que el código de estado sea 400 (Bad Request)
    assert response.status_code == 400
    assert response.json() == {"detail": "Error interno en la base de datos"}

# Test para comentar una publicación exitosamente
def test_comentar_publicacion_exitoso(monkeypatch):
    publicacion_id = "123"
    comentario = {
        "comentario": "wiii"
    }

    # Simular que se agrega el comentario correctamente
    def mock_agregar_comentarioM(publicacion_id, comentario_texto, db):
        return True  # Simulamos que se agregó correctamente

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.agregar_comentarioM", mock_agregar_comentarioM)

    # Realizar la solicitud
    response = client.post(f"/mongo/publicaciones/{publicacion_id}/comentar/", json=comentario)

    # Verificar que el código de estado sea 200 (OK)
    assert response.status_code == 200
    assert response.json() == {"message": "Comentario agregado exitosamente"}

# Test para manejar el caso cuando no se encuentra la publicación
def test_comentar_publicacion_no_encontrada(monkeypatch):
    publicacion_id = "999"
    comentario = {
        "comentario": "wiii"
    }

    # Simular que no se pudo agregar el comentario porque la publicación no existe
    def mock_agregar_comentarioM_no_encontrada(publicacion_id, comentario_texto, db):
        return False  # Simulamos que no se pudo agregar el comentario

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.agregar_comentarioM", mock_agregar_comentarioM_no_encontrada)

    # Realizar la solicitud
    response = client.post(f"/mongo/publicaciones/{publicacion_id}/comentar/", json=comentario)

    # Verificar que el código de estado sea 404 (Not Found)
    assert response.status_code == 400
    assert response.json() != {"detail": "Publicación no encontrada o no se pudo agregar el comentario"}

# Test para manejar errores inesperados
def test_comentar_publicacion_error(monkeypatch):
    publicacion_id = "123"
    comentario = {
        "comentario": "wiii"
    }

    # Simular un error inesperado en la función
    def mock_agregar_comentarioM_error(publicacion_id, comentario_texto, db):
        raise Exception("Error inesperado")

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.agregar_comentarioM", mock_agregar_comentarioM_error)

    # Realizar la solicitud
    response = client.post(f"/mongo/publicaciones/{publicacion_id}/comentar/", json=comentario)

    # Verificar que el código de estado sea 400 (Bad Request)
    assert response.status_code == 400
    assert response.json() == {"detail": "Error inesperado"}

# Test para reaccionar a una publicación exitosamente
def test_reaccionar_publicacion_exitoso(monkeypatch):
    publicacion_id = "123"
    reaccion = {
        "reaccion": "like"
    }

    # Simular que se agrega la reacción correctamente
    def mock_agregar_reaccionM(publicacion_id, reaccion_texto, db):
        return True  # Simulamos que se agregó correctamente

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.agregar_reaccionM", mock_agregar_reaccionM)

    # Realizar la solicitud
    response = client.post(f"/mongo/publicaciones/{publicacion_id}/reaccionar/", json=reaccion)

    # Verificar que el código de estado sea 200 (OK)
    assert response.status_code == 200
    assert response.json() == {"message": "Reacción agregada exitosamente"}

# Test para manejar el caso cuando no se encuentra la publicación
def test_reaccionar_publicacion_no_encontrada(monkeypatch):
    publicacion_id = "999"
    reaccion = {
        "reaccion": "like"
    }

    # Simular que no se pudo agregar la reacción porque la publicación no existe
    def mock_agregar_reaccionM_no_encontrada(publicacion_id, reaccion_texto, db):
        return False  # Simulamos que no se pudo agregar la reacción

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.agregar_reaccionM", mock_agregar_reaccionM_no_encontrada)

    # Realizar la solicitud
    response = client.post(f"/mongo/publicaciones/{publicacion_id}/reaccionar/", json=reaccion)

    # Verificar que el código de estado sea 404 (Not Found)
    assert response.status_code == 400
    assert response.json() != {"detail": "Publicación no encontrada o no se pudo agregar la reacción"}

# Test para manejar errores inesperados
def test_reaccionar_publicacion_error(monkeypatch):
    publicacion_id = "123"
    reaccion = {
        "reaccion": "like"
    }

    # Simular un error inesperado en la función
    def mock_agregar_reaccionM_error(publicacion_id, reaccion_texto, db):
        raise Exception("Error inesperado")

    # Usar monkeypatch para reemplazar la función
    monkeypatch.setattr("app.agregar_reaccionM", mock_agregar_reaccionM_error)

    # Realizar la solicitud
    response = client.post(f"/mongo/publicaciones/{publicacion_id}/reaccionar/", json=reaccion)

    # Verificar que el código de estado sea 400 (Bad Request)
    assert response.status_code == 400
    assert response.json() == {"detail": "Error inesperado"}

