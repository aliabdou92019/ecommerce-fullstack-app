from fastapi.testclient import TestClient
from main import app

client = TestClient(app)



def create_admin_and_login():

    client.post(
        "/api/v1/users/register",
        json={
            "username": "catadmin",
            "email": "catadmin@test.com",
            "password": "12345678",
            "role": "admin"
        }
    )

    response = client.post(
        "/api/v1/users/login",
        data={
            "username": "catadmin@test.com",
            "password": "12345678"
        }
    )

    token = response.json()["access_token"]

    return token




def test_create_category():

    token = create_admin_and_login()

    response = client.post(
        "/api/v1/categories/add",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Electronics",
            "description": "Electronic devices"
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Electronics"




def test_get_categories():

    response = client.get("/api/v1/categories/getall")

    assert response.status_code == 200
    assert isinstance(response.json(), list)




def test_get_category_by_id():

    response = client.get("/api/v1/categories/1")

    assert response.status_code in [200, 404]



def test_edit_category():

    token = create_admin_and_login()

    # create category first
    create_response = client.post(
        "/api/v1/categories/add",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Mobiles",
            "description": "Phones"
        }
    )

    category_id = create_response.json()["id"]

    # edit category
    response = client.put(
        f"/api/v1/categories/{category_id}",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Smart Phones"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Smart Phones"



def test_delete_category():

    token = create_admin_and_login()

    
    create_response = client.post(
        "/api/v1/categories/add",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "name": "Accessories",
            "description": "Accessories category"
        }
    )

    category_id = create_response.json()["id"]


    response = client.delete(
        f"/api/v1/categories/{category_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Category deleted"



def test_create_category_unauthorized():

    response = client.post(
        "/api/v1/categories/add",
        json={
            "name": "Unauthorized",
            "description": "Test"
        }
    )

    assert response.status_code in [401, 403]