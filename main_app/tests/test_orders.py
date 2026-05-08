from fastapi.testclient import TestClient
from main import app

client = TestClient(app)



def create_admin_and_login():

    client.post(
        "/api/v1/users/register",
        json={
            "username": "orderadmin",
            "email": "orderadmin@test.com",
            "password": "12345678",
            "role": "admin"
        }
    )

    response = client.post(
        "/api/v1/users/login",
        data={
            "username": "orderadmin@test.com",
            "password": "12345678"
        }
    )

    return response.json()["access_token"]


def create_user_and_login():

    client.post(
        "/api/v1/users/register",
        json={
            "username": "orderuser",
            "email": "orderuser@test.com",
            "password": "12345678",
            "role": "user"
        }
    )

    response = client.post(
        "/api/v1/users/login",
        data={
            "username": "orderuser@test.com",
            "password": "12345678"
        }
    )

    return response.json()["access_token"]


def create_category(admin_token):

    response = client.post(
        "/api/v1/categories/add",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name": "OrdersCategory",
            "description": "Orders category"
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
            "name": "Order Product",
            "description": "Testing product",
            "price": 500,
            "stock": 20,
            "category_id": category_id
        }
    )

    return response.json()["id"]


def add_product_to_cart(user_token, product_id):

    client.post(
        "/api/v1/cart/",
        headers={
            "Authorization": f"Bearer {user_token}"
        },
        json={
            "product_id": product_id,
            "quantity": 2
        }
    )



def test_create_order():

    admin_token = create_admin_and_login()

    user_token = create_user_and_login()

    category_id = create_category(admin_token)

    product_id = create_product(admin_token, category_id)

    add_product_to_cart(user_token, product_id)

    response = client.post(
        "/api/v1/orders/create",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )

    assert response.status_code == 201



def test_get_my_orders():

    token = create_user_and_login()

    response = client.get(
        "/api/v1/orders/get/my_orders",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code in [200, 404]



def test_get_all_orders():

    admin_token = create_admin_and_login()

    response = client.get(
        "/api/v1/orders/get_all_orders",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code in [200, 404]



def test_get_user_orders():

    admin_token = create_admin_and_login()

    response = client.get(
        "/api/v1/orders/get/user/1",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code in [200, 404]



def test_cancel_order():

    admin_token = create_admin_and_login()

    user_token = create_user_and_login()

    category_id = create_category(admin_token)

    product_id = create_product(admin_token, category_id)

    add_product_to_cart(user_token, product_id)

    create_response = client.post(
        "/api/v1/orders/create",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )

    order_id = create_response.json()["id"]

    response = client.delete(
        f"/api/v1/orders/cancel/{order_id}",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )

    assert response.status_code == 200



def test_ship_order():

    admin_token = create_admin_and_login()

    user_token = create_user_and_login()

    category_id = create_category(admin_token)

    product_id = create_product(admin_token, category_id)

    add_product_to_cart(user_token, product_id)

    create_response = client.post(
        "/api/v1/orders/create",
        headers={
            "Authorization": f"Bearer {user_token}"
        }
    )

    order_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/orders/put/ship/{order_id}",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200



def test_orders_unauthorized():

    response = client.get("/api/v1/orders/get_all_orders")

    assert response.status_code in [401, 403]