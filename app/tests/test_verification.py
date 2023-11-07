import pytest
from fastapi.testclient import TestClient
from main import app
from fastapi import status
from repository.user_repository import UserRepository
from utils.auth import generate_and_hash_verification_code
import os
from config.database import Database
from datetime import datetime, timedelta

client = TestClient(app)

TEST_EMAIL = "test_signup@example.com"
TEST_PASSWORD = "testpassword"
TEST_EMAIL_EXISTING = "test_signup_existing_user@example.com"
(
    TEST_RIGHT_VERIFICATION_CODE,
    TEST_HASHED_VERIFICATION_CODE,
) = generate_and_hash_verification_code()
TEST_WRONG_VERIFICATION_CODE = "4321"


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
    user_repository.delete_user(TEST_EMAIL)
    user_repository.delete_user(TEST_EMAIL_EXISTING)


def test_verification(get_user_repository):
    user_repository = get_user_repository
    signup_response = client.post(
        "/signup", json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
    )
    assert signup_response.status_code == status.HTTP_201_CREATED

    # Update the user in the database with the hashed verification code for the test
    stored_user = user_repository.get_user_by_email(TEST_EMAIL)
    stored_user.verification_code = TEST_HASHED_VERIFICATION_CODE
    user_repository.update_verification_code(TEST_HASHED_VERIFICATION_CODE, stored_user)

    response = client.post(
        "/verify",
        json={"email": TEST_EMAIL, "verification_code": TEST_RIGHT_VERIFICATION_CODE},
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "User verified successfully"}
    stored_user = user_repository.get_user_by_email(TEST_EMAIL)
    assert stored_user.is_verified == True


def test_verification_with_wrong_code(get_user_repository):
    user_repository = get_user_repository
    signup_response = client.post(
        "/signup", json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
    )
    assert signup_response.status_code == status.HTTP_201_CREATED

    # Update the user in the database with the hashed verification code for the test
    stored_user = user_repository.get_user_by_email(TEST_EMAIL)
    stored_user.verification_code = TEST_HASHED_VERIFICATION_CODE
    user_repository.update_verification_code(TEST_HASHED_VERIFICATION_CODE, stored_user)

    response = client.post(
        "/verify",
        json={"email": TEST_EMAIL, "verification_code": TEST_WRONG_VERIFICATION_CODE},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "The verification code you entered does not match our records."
    }

    stored_user = user_repository.get_user_by_email(TEST_EMAIL)
    assert stored_user.is_verified == False


def test_verification_code_expiry(get_user_repository):
    user_repository = get_user_repository
    signup_response = client.post(
        "/signup", json={"email": TEST_EMAIL, "password": TEST_PASSWORD}
    )
    assert signup_response.status_code == status.HTTP_201_CREATED

    # Update the user in the database with the hashed verification code for the test
    stored_user = user_repository.get_user_by_email(TEST_EMAIL)
    stored_user.verification_code = TEST_HASHED_VERIFICATION_CODE
    user_repository.update_verification_code(TEST_HASHED_VERIFICATION_CODE, stored_user)

    # Simulate the passage of time by setting the expiry time to the past
    past_time = datetime.now() - timedelta(minutes=1)
    user_repository.update_verification_code_expiry(past_time, stored_user)

    response = client.post(
        "/verify",
        json={"email": TEST_EMAIL, "verification_code": TEST_RIGHT_VERIFICATION_CODE},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "detail": "The verification code has expired. Please request a new one."
    }

    stored_user = user_repository.get_user_by_email(TEST_EMAIL)
    assert stored_user.is_verified == False
