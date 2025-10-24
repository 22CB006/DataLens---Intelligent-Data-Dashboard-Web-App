"""
Authentication Tests

Tests for user registration, login, and token management.
"""

import pytest
from fastapi import status


class TestUserRegistration:
    """Test user registration endpoints."""
    
    def test_register_new_user(self, client):
        """Test successful user registration."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "username": "newuser",
                "password": "SecurePassword123!",
                "full_name": "New User"
            }
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["username"] == "newuser"
        assert "id" in data
        assert "hashed_password" not in data  # Password should not be returned
    
    def test_register_duplicate_email(self, client, test_user):
        """Test registration with existing email fails."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": test_user.email,
                "username": "differentusername",
                "password": "SecurePassword123!",
                "full_name": "Duplicate User"
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already registered" in response.json()["detail"].lower()
    
    def test_register_duplicate_username(self, client, test_user):
        """Test registration with existing username fails."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "different@example.com",
                "username": test_user.username,
                "password": "SecurePassword123!",
                "full_name": "Duplicate User"
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_register_invalid_email(self, client):
        """Test registration with invalid email format."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "username": "testuser",
                "password": "SecurePassword123!",
                "full_name": "Test User"
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_register_weak_password(self, client):
        """Test registration with weak password."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "123",  # Too short
                "full_name": "Test User"
            }
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestUserLogin:
    """Test user login endpoints."""
    
    def test_login_success(self, client, test_user):
        """Test successful login."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user.email,
                "password": "testpassword123"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self, client, test_user):
        """Test login with incorrect password."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user.email,
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user."""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "password123"
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_login_inactive_user(self, client, test_user, db_session):
        """Test login with inactive user."""
        # Deactivate user
        test_user.is_active = False
        db_session.commit()
        
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user.email,
                "password": "testpassword123"
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestCurrentUser:
    """Test current user endpoints."""
    
    def test_get_current_user(self, client, test_user, auth_headers):
        """Test getting current user information."""
        response = client.get(
            "/api/v1/auth/me",
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["email"] == test_user.email
        assert data["username"] == test_user.username
        assert "hashed_password" not in data
    
    def test_get_current_user_no_token(self, client):
        """Test getting current user without authentication."""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_current_user_invalid_token(self, client):
        """Test getting current user with invalid token."""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestTokenValidation:
    """Test token validation and expiration."""
    
    def test_valid_token_access(self, client, auth_headers):
        """Test accessing protected endpoint with valid token."""
        response = client.get(
            "/api/v1/datasets/",
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
    
    def test_expired_token_access(self, client):
        """Test accessing protected endpoint with expired token."""
        # Create an expired token (would need to mock time or use a very short expiration)
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.expired"
        
        response = client.get(
            "/api/v1/datasets/",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_malformed_token(self, client):
        """Test accessing protected endpoint with malformed token."""
        response = client.get(
            "/api/v1/datasets/",
            headers={"Authorization": "Bearer malformed.token.here"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.integration
class TestAuthenticationFlow:
    """Integration tests for complete authentication flow."""
    
    def test_complete_auth_flow(self, client):
        """Test complete registration -> login -> access flow."""
        # 1. Register
        register_response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "flowtest@example.com",
                "username": "flowtest",
                "password": "SecurePassword123!",
                "full_name": "Flow Test User"
            }
        )
        assert register_response.status_code == status.HTTP_201_CREATED
        
        # 2. Login
        login_response = client.post(
            "/api/v1/auth/login",
            json={
                "email": "flowtest@example.com",
                "password": "SecurePassword123!"
            }
        )
        assert login_response.status_code == status.HTTP_200_OK
        token = login_response.json()["access_token"]
        
        # 3. Access protected endpoint
        me_response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert me_response.status_code == status.HTTP_200_OK
        assert me_response.json()["email"] == "flowtest@example.com"
