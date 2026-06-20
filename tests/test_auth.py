import pytest
import uuid 
import token

@pytest.fixture
def registered_user(client):
    user_data = {
        "email": f"test_{uuid.uuid4().hex[:8]}@example.com",
        "full_name": "tested one",
        "password": "1235"
    }
    response = client.post("/auth/register", json=user_data)
    return response.json()



def test_register_success(client):
    user_data = {
        "email": "test@example.com",
        "full_name": "tested one",
        "password": "1235"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

def test_register_duplicate_email(client):
    user_data = {
        "email": "test@example.com",
        "full_name": "tested one",
        "password": "1235"
    }
    response = client.post("/auth/register", json=user_data)
    response_s = client.post("/auth/register", json=user_data)
    assert response_s.status_code == 400

def test_login_success(client, registered_user):
    params={"email":registered_user["email"] , "password": "1235"}
    response = client.post("/auth/login", params=params)
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_login_wrong_password(client, registered_user):
    params={"email":registered_user["email"] , "password": "126"}
    response = client.post("/auth/login", params=params)
    assert response.status_code == 401

def test_me(client, registered_user):
    params={"email":registered_user["email"] , "password": "1235"}
    response = client.post("/auth/login", params=params)
    token = response.json()["access_token"]
    me_response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert registered_user["email"] == me_response.json()["email"] 

def test_logout(client, registered_user):
    params={"email":registered_user["email"] , "password": "1235"}
    response = client.post("/auth/login", params=params)
    token = response.json()["access_token"]
    logout_response = client.post("/auth/logout", json={"access_token": token})
    assert logout_response.status_code == 422

def test_refresh(client, registered_user):
    params={"email":registered_user["email"] , "password": "1235"}
    response = client.post("/auth/login", params=params)
    token = response.json()["refresh_token"]
    refresh_response = client.post("/auth/refresh", json={"refresh_token": token})
    assert "refresh_token" in response.json()

def test_revoke(client, registered_user):
    params={"email":registered_user["email"] , "password": "1235"}
    response = client.post("/auth/login", params=params)
    print(response.json())
    token = response.json()["refresh_token"]
    revoke_response = client.post("/auth/revoke", json={"refresh_token": token})
    assert revoke_response.status_code == 422
