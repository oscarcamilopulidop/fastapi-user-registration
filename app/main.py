from fastapi import FastAPI

from routers.verify_user import verify_user_router
from routers.signup import signup_router

from routers.login import login_router
from routers.code_generator import code_generator
from middleware.error_handler import ErrorHandler


app = FastAPI()
app.title = "User registration API"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

app.include_router(verify_user_router)
app.include_router(signup_router)
app.include_router(login_router)
app.include_router(code_generator)
