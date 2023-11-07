from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from schemas.user import VerificationUser
from dependencies import get_verification_service
from services.verification_service import VerificationService

verify_user_router = APIRouter()


@verify_user_router.post("/verify", response_model=dict, status_code=200)
async def verify_user(
    user: VerificationUser,
    verification_service: VerificationService = Depends(get_verification_service),
):
    response = verification_service.verify_user(user)
    return JSONResponse(status_code=200, content=response)
