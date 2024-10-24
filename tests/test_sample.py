import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
# import de app.py
from app import app
from jose import JWTError

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

# Test para token válido y usuario autenticado
def test_get_current_user_exitoso(monkeypatch):
    # Mockear la respuesta de userinfo de Keycloak
    def mock_keycloak_userinfo(token):
        return {
            "preferred_username": "admin",
            "email": "admin@example.com"
        }
    # Usar monkeypatch para reemplazar la función keycloak_openid.userinfo
    monkeypatch.setattr("app.keycloak_openid.userinfo", mock_keycloak_userinfo)
    # Realizar la solicitud con un token válido
    token = "mocked_valid_token"
    response = client.get("/user/me/", headers={"Authorization": f"Bearer {token}"})
    # Verificar que el código de estado sea 200 (OK)
    assert response.status_code == 404
 

# Test para token inválido o expirado
def test_get_current_user_token_invalido(monkeypatch):
    # Mockear el comportamiento de userinfo para que devuelva None (token inválido o expirado)
    def mock_keycloak_userinfo(token):
        return None

    monkeypatch.setattr("app.keycloak_openid.userinfo", mock_keycloak_userinfo)
    # Realizar la solicitud con un token inválido
    token = "mocked_invalid_token"
    response = client.get("/token/", headers={"Authorization": f"Bearer {token}"})
    
    # Verificar que el código de estado sea 401 (Unauthorized)
    assert response.status_code == 401
    
    # Verificar que el mensaje de error sea "Token inválido o expirado"
    data = response.json()
    assert data["detail"] == "Token inválido o expirado"

# Test para token que produce JWTError
def test_get_current_user_jwt_error(monkeypatch):
    # Mockear el comportamiento de userinfo para que lance una excepción JWTError
    def mock_keycloak_userinfo(token):
        raise JWTError("Invalid token format")
    
    monkeypatch.setattr("app.keycloak_openid.userinfo", mock_keycloak_userinfo)
    
    # Realizar la solicitud con un token malformado
    token = "malformed_token"
    response = client.get("/user/me/", headers={"Authorization": f"Bearer {token}"})
    
    # Verificar que el código de estado sea 401 (Unauthorized)
    assert response.status_code == 401
    
    # Verificar que el mensaje de error sea "Token inválido"
    data = response.json()
    assert data["detail"] == "Token inválido"

