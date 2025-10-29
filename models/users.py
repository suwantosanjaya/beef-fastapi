from sqlalchemy import Column, String, Boolean
from core.database import Base
from models.base_mixin import BaseMixin

class Users(BaseMixin, Base):
    __tablename__ = "users"

    username = Column(String(100), unique=True, nullable=False)
    fullname = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    google_id = Column(String(255), unique=True, nullable=True)
    avatar = Column(String(255), nullable=True)
    active = Column(Boolean, default=False)
    
    # institusi = relationship(
    #     "Institusi",
    #     back_populates="user",
    #     foreign_keys="[Institusi.created_by]"  # <-- tambahkan ini
    # )
    