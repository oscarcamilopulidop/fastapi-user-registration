from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Union
from fastapi.exceptions import RequestValidationError
from services.email_service import EmailSendingFailed


class ErrorHandler(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)

    async def dispatch(
        self, request: Request, call_next
    ) -> Union[Response, JSONResponse]:
        try:
            return await call_next(request)
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"error": e.detail})
        except StarletteHTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"error": e.detail})
        except RequestValidationError as e:
            return JSONResponse(status_code=422, content={"error": e.errors()})
        except EmailSendingFailed as e:
            return JSONResponse(status_code=500, content={"error": str(e)})
        except Exception as e:
            return JSONResponse(
                status_code=500, content={"error": "An unexpected error occurred"}
            )
