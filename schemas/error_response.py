from pydantic import BaseModel

class ErrorResponse(BaseModel):
    status: bool
    message: str
    errors: dict = {}
    