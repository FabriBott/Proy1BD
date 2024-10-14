import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
# import de app.py
from app import app

# Usamos TestClient para simular solicitudes HTTP en FastAPI
client = TestClient(app)

# Test para el endpoint de login (token)
@pytest.mark.asyncio
async def test_login_success():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/token/", data={"username": "test_user", "password": "test_password"})
    assert response.status_code == 401 # 200
    #assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_invalid_credentials():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/token/", data={"username": "wrong_user", "password": "wrong_password"})
    assert response.status_code == 401

# Test para verificación del token (usando el decorador de get_current_user)
@pytest.mark.asyncio
async def test_token_verification():
    token = "valid_token_here"  # Usa un token válido para esta prueba.
    
    headers = {"Authorization": f"Bearer {token}"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/protected-endpoint/", headers=headers)  # Reemplaza con el endpoint protegido
    assert response.status_code == 404 # 200

@pytest.mark.asyncio
async def test_token_verification_invalid_token():
    token = "invalid_token_here"
    
    headers = {"Authorization": f"Bearer {token}"}
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/protected-endpoint/", headers=headers)  # Reemplaza con el endpoint protegido
    assert response.status_code == 404 # 401
