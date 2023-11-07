import pytest
from fastapi.testclient import TestClient
from main import app
from fastapi import status
from repository.user_repository import UserRepository
import os
from config.database import Database

client = TestClient(app)

TEST_EMAIL = "test_signup@example.com"
TEST_PASSWORD = "testpassword"
TEST_EMAIL_EXISTING = "test_signup_existing_user@example.com"


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
    user_repository = UserRepository(get_database)
    yield user_repository
    # Cleanup
    user_repository.delete_user(TEST_EMAIL)
    user_repository.delete_user(TEST_EMAIL_EXISTING)


def test_signup(get_user_repository):
    user_repository = get_user_repository
    response = client.post(
        "/signup", json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "message": "If your email is not registered yet, you will receive an email with the activation code"
    }
    assert user_repository.user_exists(TEST_EMAIL)


def test_signup_existing_user(get_user_repository):
    get_user_repository
    client.post(
        "/signup", json={"email": TEST_EMAIL_EXISTING, "password": TEST_PASSWORD}
    )
    response = client.post(
        "/signup", json={"email": TEST_EMAIL_EXISTING, "password": TEST_PASSWORD}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        "message": "If your email is not registered yet, you will receive an email with the activation code"
    }


def test_verification_code_generated(get_user_repository):
    user_repository = get_user_repository
    client.post("/signup", json={"email": TEST_EMAIL, "password": TEST_PASSWORD})
    user_registered = user_repository.get_user_by_email(TEST_EMAIL)
    assert user_registered.verification_code is not None
    assert user_registered.verification_code_expiry is not None
