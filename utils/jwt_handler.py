from datetime import datetime, timedelta, timezone
from fastapi import Request
from jose import jwt, JWTError
from exceptions.custom_exception import CustomException
from core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict, user_agent: str):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire, 
        "type": "access",
        "user_agent": user_agent
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, user_agent: str):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": expire,
        "type": "refresh",
        "user_agent": user_agent
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Verifikasi JWT
def verify_token(token: str, current_user_agent: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_user_agent = payload.get("user_agent")
        if token_user_agent != current_user_agent:
            raise CustomException(status_code=401, message="User-Agent mismatch")
        return payload
    except JWTError:
        return None
    
def get_current_email_from_token(request: Request) -> str:
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise CustomException(status_code=401, message="Missing or invalid token")
    
    token = auth.split(" ")[1]
    # payload = decode_jwt(token)
    user_agent = request.headers.get("User-Agent", "")
    payload = verify_token(token, user_agent)
    if not payload:
        raise CustomException(status_code=401, message="Invalid token")
    return payload.get("sub")  # `sub` is usually the email