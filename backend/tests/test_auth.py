from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch
from app.utils.auth_utils import create_access_token

client = TestClient(app)

def test_signup():
    response = client.post("/api/v1/auth/signup", json={
        "email": "unique_user@example.com",  # Use a unique email
        "password": "password123",
        "name": "Test User"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"

def test_login():
    # Ensure the user exists before testing login
    client.post("/api/v1/auth/signup", json={
        "email": "unique_user@example.com",
        "password": "password123",
        "name": "Test User"
    })
    response = client.post("/api/v1/auth/login", json={
        "email": "unique_user@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

@patch("app.utils.email.send_password_reset_email")  # Mock email sending
def test_forgot_password(mock_send_email):
    # Ensure the user exists before testing forgot-password
    client.post("/api/v1/auth/signup", json={
        "email": "unique_user@example.com",
        "password": "password123",
        "name": "Test User"
    })
    mock_send_email.return_value = None  # Mock the email sending function
    response = client.post("/api/v1/auth/forgot-password", json={
        "email": "unique_user@example.com"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Password reset email sent"
    mock_send_email.assert_called_once()

def test_reset_password():
    # Ensure the user exists before testing reset-password
    client.post("/api/v1/auth/signup", json={
        "email": "unique_user@example.com",
        "password": "password123",
        "name": "Test User"
    })
    # Generate a valid reset token
    reset_token = create_access_token({"sub": "unique_user@example.com"})
    response = client.post("/api/v1/auth/reset-password", json={
        "token_data": {"sub": "unique_user@example.com"},
        "new_password": "newpassword123"
    })
    assert response.status_code == 200
    assert response.json()["message"] == "Password reset successfully"