from schemas.user import BaseUser, User
from repository.user_repository import UserRepository
from services.email_service import EmailService
from utils.auth import generate_and_hash_verification_code


class SignupService:
    def __init__(
        self, user_repository: UserRepository, email_service: EmailService
    ) -> None:
        self.user_repository = user_repository
        self.email_service = email_service

    def signup_user(self, user: BaseUser):
        if not (self.user_repository.user_exists(user.email)):
            (
                verification_code,
                hashed_verification_code,
            ) = self._generate_verification_code()
            new_user = self._create_new_user(user, hashed_verification_code)
            self.user_repository.register_new_user(new_user)
            self.email_service.send_verification_email(user, verification_code)

        return {
            "message": "If your email is not registered yet, you will receive an email with the activation code"
        }

    def _generate_verification_code(self):
        return generate_and_hash_verification_code()

    def _create_new_user(self, user: BaseUser, hashed_verification_code: str) -> User:
        return User(**user.dict(), verification_code=hashed_verification_code)
