from datetime import datetime
from schemas.user import VerificationUser
from fastapi import HTTPException, status
import hashlib
from repository.user_repository import UserRepository
from utils.auth import generate_and_hash_verification_code
from services.email_service import EmailService


class VerificationService:
    def __init__(
        self, user_repository: UserRepository, email_service: EmailService
    ) -> None:
        self.user_repository = user_repository
        self.email_service = email_service

    def generate_verification_code(self, user: VerificationUser):
        stored_user = self.user_repository.get_user_by_email_or_404(user.email)
        self._check_verified_user(stored_user)
        (
            verification_code,
            hashed_verification_code,
        ) = self._generate_and_store_verification_code(stored_user)
        self._send_verification_email(user, verification_code)
        return {
            "message": "Verification code generated successfully, please check your email for the verification code"
        }

    def _check_verified_user(self, stored_user):
        if stored_user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This account is already verified",
            )

    def verify_user(self, user: VerificationUser):
        stored_user = self.user_repository.get_user_by_email_or_404(user.email)
        self._check_verification_code(user, stored_user)
        self._check_verification_code_expiry(stored_user)
        self._verify_user(stored_user)
        return {"message": "User verified successfully"}

    def _check_verification_code(self, user: VerificationUser, stored_user):
        hashed_verification_code = hashlib.sha256(
            str(user.verification_code).encode()
        ).hexdigest()
        if stored_user.verification_code != hashed_verification_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The verification code you entered does not match our records.",
            )

    def _generate_and_store_verification_code(self, stored_user):
        (
            verification_code,
            hashed_verification_code,
        ) = generate_and_hash_verification_code()
        stored_user.verification_code = hashed_verification_code
        self.user_repository.update_verification_code(
            hashed_verification_code, stored_user
        )
        return verification_code, hashed_verification_code

    def _send_verification_email(self, user, verification_code):
        self.email_service.send_verification_email(user, verification_code)

    def _check_verification_code_expiry(self, stored_user):
        if datetime.utcnow() > stored_user.verification_code_expiry:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The verification code has expired. Please request a new one.",
            )

    def _verify_user(self, stored_user):
        stored_user.is_verified = True
        self.user_repository.update_verified_user(stored_user)
