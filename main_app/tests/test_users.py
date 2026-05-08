from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_register():
    response = client.post(
        "/api/v1/users/register",
        json={
            "username": "testuser1",
            "email": "test1@test.com",
            "password": "12345678",
            "role": "user"
        }
    )

    assert response.status_code == 201


def test_login():

    # create user first
    client.post(
        "/api/v1/users/register",
        json={
            "username": "loginuser",
            "email": "login@test.com",
            "password": "12345678",
            "role": "user"
        }
    )

    response = client.post(
        "/api/v1/users/login",
        data={
            "username": "login@test.com",
            "password": "12345678"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_get_me():

    client.post(
        "/api/v1/users/register",
        json={
            "username": "meuser",
            "email": "me@test.com",
            "password": "12345678",
            "role": "user"
        }
    )

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "me@test.com",
            "password": "12345678"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_get_my_role():

    client.post(
        "/api/v1/users/register",
        json={
            "username": "roleuser",
            "email": "role@test.com",
            "password": "12345678",
            "role": "user"
        }
    )

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "role@test.com",
            "password": "12345678"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/api/v1/users/me/role",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["role"] == "user"



def test_edit_user():

    client.post(
        "/api/v1/users/register",
        json={
            "username": "edituser",
            "email": "edit@test.com",
            "password": "12345678",
            "role": "user"
        }
    )

    login_response = client.post(
        "/api/v1/users/login",
        data={
            "username": "edit@test.com",
            "password": "12345678"
        }
    )

    token = login_response.json()["access_token"]

    response = client.put(
        "/api/v1/users/edit",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "username": "editeduser"
        }
    )

    assert response.status_code == 200
    assert response.json()["username"] == "editeduser"


def test_get_users_unauthorized():

    response = client.get("/api/v1/users/")

    assert response.status_code in [401, 403]