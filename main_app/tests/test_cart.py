from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_unauthorized_cart_access():

    response = client.get("/api/v1/cart")

    assert response.status_code == 401