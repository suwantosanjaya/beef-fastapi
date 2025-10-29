from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from schemas.user_schema import UserRequest, UserResponse, Token
from schemas.api_response import APIResponse
from services.auth_service import AuthService
from core.database import get_db
from core.config import REFRESH_TOKEN_EXPIRE_MINUTES
from exceptions.custom_exception import CustomException

router = APIRouter(prefix="/auth", tags=["Authentication"])

class AuthController:
    def __init__(self):
        self.router = router
        self.setup_routes()

    def setup_routes(self):               
        @self.router.post("/login", response_model=Token, response_model_exclude_none=True)
        def login(user_create: UserRequest, response: Response, request: Request, db: Session = Depends(get_db)):
            service = AuthService(db)
            user = service.authenticate_user(user_create.email, user_create.password)
            if not user:
                raise HTTPException(status_code=401, detail="Invalid credentials")

            user_agent = request.headers.get("User-Agent")
            token = service.generate_access_token(user=user, user_agent=user_agent)
            refresh_token = service.generate_refresh_token(user=user, user_agent=user_agent)
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,      # wajib True di production (HTTPS)
                samesite="lax",   # atau "strict"
                max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,  # dalam detik
            )
            return {"access_token": token}

        @self.router.post("/refresh", response_model=Token, response_model_exclude_none=True,)
        def refresh_token(request: Request, db: Session = Depends(get_db)):
            service = AuthService(db)
            refresh_token = request.cookies.get("refresh_token")
            user_agent = request.headers.get("User-Agent", "")
            if not refresh_token:
                raise CustomException(status_code=401, message="Refresh token not found")
            
            user = service.get_user_by_refresh_token(refresh_token, user_agent)
            if not user:
                raise CustomException(status_code=401, message="Invalid refresh token")
            new_access_token = service.generate_access_token(user=user, user_agent=user_agent)
            return {"access_token": new_access_token}
        
        @self.router.post("/logout", response_model=APIResponse[dict], response_model_exclude_none=True)
        def logout(response: Response):
            response.delete_cookie("refresh_token")
            return APIResponse(
                status=True,
                message="Logout successful",
                data=None
            )
        
        @self.router.post("/register", response_model=UserResponse, response_model_exclude_none=True)
        def register(user_create: UserRequest, db: Session = Depends(get_db)):
            service = AuthService(db)
            existing = service.get_user_by_email(user_create.email)
            if existing:
                raise HTTPException(status_code=400, detail="Email already exists")
            return service.create_user(user_create)
        
        @self.router.get("/me", response_model=UserResponse, response_model_exclude_none=True)
        def get_current_user(request: Request, db: Session = Depends(get_db)):
            # service = AuthService(db)
            # user = service.get_user_by_token(request)
            # if not user:
            #     raise ObeException(status_code=401, message="User not found")
            # return user
            pass
