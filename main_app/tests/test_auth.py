from fastapi.testclient import TestClient
from main_app.main import app

client = TestClient(app)

def test_register():

    response = client.post(
        "/api/v1/users/register",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "12345678",
            "role": "user"
        }
    )

    assert response.status_code == 201