def test_login():

    response = client.post(
        "/api/v1/users/login",
        data={
            "username": "test@test.com",
            "password": "12345678"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()