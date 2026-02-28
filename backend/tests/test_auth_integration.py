import pytest

@pytest.fixture
def test_user():
    return {
        "email": "test@example.com",
        "password": "password123"  # <= 72 chars
    }

def test_register(client, test_user):
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 200
    data = response.json()
    # tokens returned correctly
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_login(client, registered_user, test_user):
    # User is already registered by the fixture!
    response = client.post("/auth/login", json=test_user)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_route(client, test_user):
    response = client.post("/auth/register", json=test_user)
    access_token = response.json()["access_token"]

    # test protected endpoint
    response = client.get(
        "/users/me/continue_watching",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

def test_refresh_rotation(client, test_user):
    client.post("/auth/register", json=test_user)
    login = client.post("/auth/login", json=test_user)
    refresh_token = login.json()["refresh_token"]

    # first refresh
    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

    new_refresh_token = data["refresh_token"]

    # old refresh should fail
    second_attempt = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert second_attempt.status_code == 401

    # new refresh should work
    valid_attempt = client.post("/auth/refresh", json={"refresh_token": new_refresh_token})
    assert valid_attempt.status_code == 200

def test_logout(client, test_user):
    client.post("/auth/register", json=test_user)
    login = client.post("/auth/login", json=test_user)
    refresh_token = login.json()["refresh_token"]

    logout = client.post("/auth/logout", json={"refresh_token": refresh_token})
    assert logout.status_code == 200
    assert logout.json()["message"] == "Logged out successfully"

    # old refresh token should now fail
    refresh_attempt = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_attempt.status_code == 401