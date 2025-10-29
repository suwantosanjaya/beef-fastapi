from sqlalchemy import Column, String
from core.database import Base
from models.base_mixin import BaseMixin

class Roles(BaseMixin, Base):
    __tablename__ = "roles"

    role_name = Column(String(255), unique=True, nullable=False)
    description = Column(String(255), nullable=True)