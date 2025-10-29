from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from schemas.error_response import ErrorResponse
from exceptions.custom_exception import CustomException

async def obe_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(status=False, message=exc.message).model_dump(),
    )

async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}
    for err in exc.errors():
        loc = err.get("loc")
        if loc and len(loc) > 1:
            field = loc[1]
            errors[field] = err.get("msg")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            status=False,
            message="Validation Error",
            errors=errors
        ).model_dump(),
    )

async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    errors = {}
    for err in exc.errors():
        loc = err.get("loc")
        if loc and len(loc) > 0:
            field = loc[-1]
            errors[field] = err.get("msg")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ErrorResponse(
            status=False,
            message="Validation Error",
            errors=errors
        ).model_dump(),
    )