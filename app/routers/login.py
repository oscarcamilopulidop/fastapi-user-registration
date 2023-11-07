from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from schemas.user import BaseUser
from dependencies import get_login_service
from services.login_service import LoginService

login_router = APIRouter()


@login_router.post("/login", response_model=dict, status_code=200)
async def login(
    user: BaseUser, login_service: LoginService = Depends(get_login_service)
):
    response = login_service.login_user(user)
    return JSONResponse(status_code=200, content=response)
