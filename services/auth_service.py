from fastapi import Request
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.users import Users
from schemas.user_schema import UserRequest
from utils.jwt_handler import create_access_token, create_refresh_token, get_current_email_from_token, verify_token
from exceptions.custom_exception import CustomException
from repositories.auth_repository import AuthRepository
from core.database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: Session = None):
        self.db = db
        self.repo = AuthRepository(db)        

    def get_user_by_email(self, email: str):
        return self.db.query(Users).filter(Users.email == email).first()

    def create_user(self, user_create: UserRequest):
        hashed_pw = pwd_context.hash(user_create.password)
        user = Users(username=user_create.email, password=hashed_pw)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate_user(self, email: str, password: str):
        user = self.get_user_by_email(email)
        if not user or not pwd_context.verify(password, user.password):
            return None
        return user

    def generate_access_token(self, user: Users, user_agent: str):
        return create_access_token(data={"sub": user.email}, user_agent=user_agent)
        
    def generate_refresh_token(self, user: Users, user_agent: str):
        return create_refresh_token(data={"sub": user.email}, user_agent=user_agent)
        
    def get_user_by_token(self, request: Request) -> Users:
        try:
            email = get_current_email_from_token(request)
            if not email:
                return None
            
            user = self.db.query(Users).filter(Users.email == email).first()
            if not user:
                return None
            return user
        except Exception as e:
            raise CustomException(status_code=401, message=f"Error fetching user by token: {str(e)}")
    def get_user_by_refresh_token(self, refresh_token: str, user_agent: str) -> Users:
        try:
            email = verify_token(refresh_token, user_agent).get("sub")
            if not email:
                return None
            
            user = self.db.query(Users).filter(Users.email == email).first()
            if not user:
                return None
            return user
        except Exception as e:
            raise CustomException(status_code=401, message=f"Error fetching user by token: {str(e)}")
