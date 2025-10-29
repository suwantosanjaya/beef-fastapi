from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class APIResponse(BaseModel, Generic[T]):
    status: bool
    message: Optional[str]
    data: Optional[T] = None
    
    class Config:
        exclude_none = True