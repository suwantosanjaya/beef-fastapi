from fastapi import Request, status
from exceptions.custom_exception import CustomException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import verify_token

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not self.verify_jwt(credentials.credentials):
                raise CustomException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    message="Invalid token or expired token.",
                )
            return credentials.credentials
        else:
            raise CustomException(
                status_code=status.HTTP_403_FORBIDDEN,
                message="Invalid authorization code.",
            )

    def verify_jwt(self, jwtoken: str) -> bool:
        payload = verify_token(jwtoken)
        return bool(payload)
