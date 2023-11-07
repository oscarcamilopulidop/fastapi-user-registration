from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from schemas.user import EmailUser
from dependencies import get_verification_service
from services.verification_service import VerificationService

code_generator = APIRouter()


@code_generator.post("/generate-activation-code", response_model=dict, status_code=200)
async def generate_code(
    user: EmailUser,
    verification_service: VerificationService = Depends(get_verification_service),
):
    response = verification_service.generate_verification_code(user)
    return JSONResponse(status_code=200, content=response)
