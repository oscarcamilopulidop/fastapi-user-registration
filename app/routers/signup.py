from fastapi import APIRouter, Depends, status
from schemas.user import BaseUser
from dependencies import get_signup_service
from utils.auth import get_password_hash
from services.signup_service import SignupService

signup_router = APIRouter()


@signup_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    user: BaseUser, signup_service: SignupService = Depends(get_signup_service)
):
    hashed_password = get_password_hash(user.password)
    user_to_create = BaseUser(email=user.email, password=hashed_password)
    response = signup_service.signup_user(user_to_create)
    return response
