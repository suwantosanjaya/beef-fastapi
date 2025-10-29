from pydantic import BaseModel

class UserRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    fullname: str

    class Config:
        from_attributes = True  # ✅ Pydantic v2
        # orm_mode = True  # Pydantic v1

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
