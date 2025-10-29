from typing import List, Optional
from fastapi import Form
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from schemas.bulk_schema import BulkResponse

from schemas.user_schema import UserResponse

class RecognitionRequest(BaseModel):
    # Request dikirim menggunakan JSON body
    id: Optional[str] = None
    nama_institusi: str = Field(..., min_length=1, max_length=255, description="Nama institusi wajib diisi")
    akronim: str = Field(..., max_length=100, description="Akronim wajib diisi")

    @classmethod
    def as_form( # Jika data dikirimkan menggunakan form data
        cls,
        id: Optional[str] = Form(None),
        nama_institusi: str = Form(..., max_length=255),
        akronim: Optional[str] = Form(..., max_length=50),
    ):
        return cls(
            id=id,
            nama_institusi=nama_institusi,
            akronim=akronim
        )


class RecognitionResponse(BaseModel):
    id: Optional[str]
    nama_institusi: Optional[str]
    akronim: Optional[str]
    logo: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    created_by_detail: Optional[UserResponse]
    updated_by_detail: Optional[UserResponse]
    deleted_by_detail: Optional[UserResponse]

    class Config:
        from_attributes = True
        exclude_none = True

