from fastapi.testclient import TestClient
from main import app

client = TestClient(app)



def create_admin_and_login():

    
    client.post(
        "/api/v1/users/register",
        json={
            "username": "adminuser",
            "email": "admin@test.com",
            "password": "12345678",
            "role": "admin"
        }
    )

    
    response = client.post(
        "/api/v1/users/login",
        data={
            "username": "admin@test.com",
            "password": "12345678"
        }
    )

    token = response.json()["access_token"]

    return token


def create_category(token):

    response = client.post(
        "/categories/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Electronics",
            "description": "الكترونيات"
        }
    )

    return response.json()["id"]


def test_create_product():

    token = create_admin_and_login()

    category_id = create_category(token)

    response = client.post(
        "/products/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "iPhone 15",
            "description": "Apple phone",
            "price": 1200,
            "stock": 5,
            "category_id": category_id
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "iPhone 15"



def test_get_products():

    response = client.get("/products/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)



def test_search_products():

    response = client.get("/products/search?name=iphone")

    assert response.status_code == 200



def test_get_product_by_id():

    response = client.get("/products/1")

    assert response.status_code in [200, 404]



def test_get_products_by_category():

    response = client.get("/products/category/1")

    assert response.status_code == 200



def test_edit_product():

    token = create_admin_and_login()

    category_id = create_category(token)

    # create product
    create_response = client.post(
        "/products/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Laptop",
            "description": "HP Laptop",
            "price": 2000,
            "stock": 10,
            "category_id": category_id
        }
    )

    product_id = create_response.json()["id"]

    # edit product
    response = client.put(
        f"/products/{product_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "price": 2500
        }
    )

    assert response.status_code == 200
    assert response.json()["price"] == 2500



def test_delete_product():

    token = create_admin_and_login()

    category_id = create_category(token)

    
    create_response = client.post(
        "/products/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Mouse",
            "description": "Gaming Mouse",
            "price": 100,
            "stock": 20,
            "category_id": category_id
        }
    )

    product_id = create_response.json()["id"]

    # delete product
    response = client.delete(
        f"/products/{product_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Product deleted successfully"



def test_create_product_unauthorized():

    response = client.post(
        "/products/",
        json={
            "name": "TV",
            "description": "Smart TV",
            "price": 3000,
            "stock": 3,
            "category_id": 1
        }
    )

    assert response.status_code in [401, 403]



def test_admin_stock_endpoint():

    token = create_admin_and_login()

    response = client.get(
        "/products/admin/stock",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200