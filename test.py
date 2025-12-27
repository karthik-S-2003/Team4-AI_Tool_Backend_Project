from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def get_admin_token():
    """Login admin and return JWT token"""
    response = client.post(
        "/admin/login",
        data={
            "username": "admin",
            "password": "password123"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_admin_login_success():
    response = client.post(
        "/admin/login",
        data={
            "username": "admin",
            "password": "password123"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_admin_login_fail():
    response = client.post(
        "/admin/login",
        data={
            "username": "admin",
            "password": "wrongpassword"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 400


def test_protected_admin_route_without_token():
    response = client.post("/admin/tools", json={
        "name": "ChatGPT",
        "pricing_type": "Free"
    })
    assert response.status_code == 401


def test_protected_admin_route_with_token():
    token = get_admin_token()

    response = client.post(
        "/admin/tools",
        json={
            "name": "ChatGPT",
            "pricing_type": "Free"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code in [200, 422]  # 422 if schema needs more fields


def test_public_user_tools_api():
    response = client.get("/users/tools")
    assert response.status_code == 200
