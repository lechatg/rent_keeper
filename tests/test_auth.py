import pytest
from httpx import AsyncClient

# @pytest.mark.asyncio(scope='session')
async def test_register_success(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": "user0@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "user0"
    })
    
    assert response.status_code == 201
    
    
async def test_register_same_email(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": "user0@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "user1"
    })
    
    assert response.status_code == 400
    
async def test_register_different_email_same_username(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": "user1@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "user0"
    })

    assert response.status_code == 400
    

async def test_register_success_with_different_username(ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": "user1@example.com",
        "password": "string",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
        "username": "user1"
    })

    assert response.status_code == 201
    

async def test_login_wrong_password(ac: AsyncClient):
    login_response = await ac.post("/auth/login", data={
        "username": "user0@example.com",
        "password": "NOTstring"
    })
    
    assert login_response.status_code == 400


async def test_login_success(ac: AsyncClient):
    # Now, log in with the registered user's credentials
    login_response = await ac.post("/auth/login", data={
        "username": "user0@example.com",
        "password": "string"
    })
    
    assert login_response.status_code == 204


async def test_check_token(ac: AsyncClient):
    login_response = await ac.post("/auth/login", data={
        "username": "user0@example.com",
        "password": "string"
    })
    # Verify that the JWT token is set in cookies
    cookies = login_response.cookies
    assert 'rent_keeper' in cookies

