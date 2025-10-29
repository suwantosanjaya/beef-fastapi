from typing import List, Optional
from pydantic import BaseModel, Field

class BulkRequest(BaseModel):
    id: List[str]

class BulkResponse(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    reason: Optional[str] = None
    
class DeleteBulkResponse(BaseModel):
    deleted: List[BulkResponse] = Field(default_factory=list)
    failed: List[BulkResponse] = Field(default_factory=list)
    
    class Config:
        exclude_none = True
