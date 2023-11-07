import pytest
from fastapi.testclient import TestClient
from main import app
from schemas.user import User
from repository.user_repository import UserRepository
from config.database import Database
from fastapi import status
import os

from utils.auth import get_password_hash

client = TestClient(app)

TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "testpassword"
TEST_ENCRYPTED_PASSWORD = get_password_hash(TEST_PASSWORD)


@pytest.fixture
def get_database():
    db = Database()
    db.initialise(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )
    return db


@pytest.fixture
def get_user_repository(get_database):
    return UserRepository(get_database)


@pytest.fixture
def test_user(get_user_repository):
    test_user = User(
        email=TEST_EMAIL,
        password=TEST_ENCRYPTED_PASSWORD,
        verification_code="1234",
        is_verified=True,
    )
    user_repository = get_user_repository
    user_repository.register_new_user(test_user)

    yield test_user

    user_repository.delete_user(test_user.email)


def test_login(test_user, get_user_repository):
    user_repository = get_user_repository
    response = client.post(
        "/login", json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    assert user_repository.user_exists(TEST_EMAIL)


def test_login_with_incorrect_credentials(test_user, get_user_repository):
    user_repository = get_user_repository
    response = client.post(
        "/login", json={"email": TEST_EMAIL, "password": "wrongpassword"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "detail" in response.json()
    assert response.json()["detail"] == "Incorrect email or password"
    assert user_repository.user_exists(TEST_EMAIL)
