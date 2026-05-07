from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_orders_unauthorized():

    response = client.get("/api/v1/orders/get_all_orders")

    assert response.status_code == 401