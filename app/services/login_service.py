from schemas.user import BaseUser
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import jwt
from utils.auth import verify_password
from repository.user_repository import UserRepository


class LoginService:
    def __init__(self, user_repository: UserRepository, secret_key: str) -> None:
        self.user_repository = user_repository
        self.secret_key = secret_key

    def login_user(self, user: BaseUser):
        stored_user = self.user_repository.get_user_by_email_or_404(user.email)
        self._check_user_verification(stored_user)
        self._check_password(user, stored_user)
        token = self._create_jwt(stored_user)
        return {"access_token": token, "token_type": "bearer"}

    def _check_user_verification(self, stored_user):
        if not stored_user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This account has not been verified",
            )

    def _check_password(self, user, stored_user):
        if not verify_password(user.password, stored_user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

    def _create_jwt(self, stored_user):
        payload = {
            "sub": stored_user.email,
            "exp": datetime.utcnow() + timedelta(days=1),
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")
