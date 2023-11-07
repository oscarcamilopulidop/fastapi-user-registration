from fastapi import Depends
from config.database import Database
import os
from services.verification_service import VerificationService
from services.email_service import EmailService
from services.signup_service import SignupService
from services.login_service import LoginService
from repository.user_repository import UserRepository


def get_database() -> Database:
    db = Database()
    db.initialise(
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
    )
    return db


def get_email_service() -> EmailService:
    return EmailService()


def get_user_repository(
    db: Database = Depends(get_database, use_cache=True),
) -> UserRepository:
    return UserRepository(db)


def get_secret_key() -> str:
    return os.getenv("JWT_SECRET_KEY")


def get_login_service(
    user_repository: UserRepository = Depends(get_user_repository),
    secret_key: str = Depends(get_secret_key),
) -> LoginService:
    return LoginService(user_repository, secret_key)


def get_signup_service(
    user_repository: UserRepository = Depends(get_user_repository),
    email_service: EmailService = Depends(get_email_service),
) -> SignupService:
    return SignupService(user_repository, email_service)


def get_verification_service(
    user_repository: UserRepository = Depends(get_user_repository),
    email_service: EmailService = Depends(get_email_service),
) -> VerificationService:
    return VerificationService(user_repository, email_service)
