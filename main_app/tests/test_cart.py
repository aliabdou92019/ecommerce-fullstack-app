from fastapi.testclient import TestClient
from main import app

client = TestClient(app)



def create_user_and_login():

    client.post(
        "/api/v1/users/register",
        json={
            "username": "cartuser",
            "email": "cart@test.com",
            "password": "12345678",
            "role": "user"
        }
    )

    response = client.post(
        "/api/v1/users/login",
        data={
            "username": "cart@test.com",
            "password": "12345678"
        }
    )

    token = response.json()["access_token"]

    return token


def create_admin_and_login():

    client.post(
        "/api/v1/users/register",
        json={
            "username": "cartadmin",
            "email": "cartadmin@test.com",
            "password": "12345678",
            "role": "admin"
        }
    )

    response = client.post(
        "/api/v1/users/login",
        data={
            "username": "cartadmin@test.com",
            "password": "12345678"
        }
    )

    token = response.json()["access_token"]

    return token


def create_category(token):

    response = client.post(
        "/api/v1/categories/add",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "CartCategory",
            "description": "Test category"
        }
    )

    return response.json()["id"]


def create_product(admin_token, category_id):

    response = client.post(
        "/products/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name": "Cart Product",
            "description": "Test Product",
            "price": 100,
            "stock": 10,
            "category_id": category_id
        }
    )

    return response.json()["id"]



def test_get_cart():

    token = create_user_and_login()

    response = client.get(
        "/api/v1/cart/",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200



def test_add_to_cart():

    admin_token = create_admin_and_login()
    user_token = create_user_and_login()

    category_id = create_category(admin_token)

    product_id = create_product(admin_token, category_id)

    response = client.post(
        "/api/v1/cart/",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "product_id": product_id,
            "quantity": 2
        }
    )

    assert response.status_code == 201



def test_update_cart_item():

    admin_token = create_admin_and_login()
    user_token = create_user_and_login()

    category_id = create_category(admin_token)

    product_id = create_product(admin_token, category_id)

    
    client.post(
        "/api/v1/cart/",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "product_id": product_id,
            "quantity": 1
        }
    )

    
    response = client.put(
        f"/api/v1/cart/{product_id}",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "quantity": 5
        }
    )

    assert response.status_code == 200




def test_remove_from_cart():

    admin_token = create_admin_and_login()
    user_token = create_user_and_login()

    category_id = create_category(admin_token)

    product_id = create_product(admin_token, category_id)

    
    client.post(
        "/api/v1/cart/",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "product_id": product_id,
            "quantity": 1
        }
    )

    
    response = client.delete(
        f"/api/v1/cart/{product_id}",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )

    assert response.status_code == 200



def test_clear_cart():

    token = create_user_and_login()

    response = client.delete(
        "/api/v1/cart/clear",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200



def test_cart_unauthorized():

    response = client.get("/api/v1/cart/")

    assert response.status_code in [401, 403]