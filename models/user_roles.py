from sqlalchemy import Column, String, ForeignKey, UniqueConstraint
from core.database import Base
from models.base_mixin import BaseMixin

class UserRoles(BaseMixin, Base):
    __tablename__ = "user_roles"

    user_id = Column(String(32), ForeignKey("users.id", onupdate="CASCADE"), primary_key=True)
    role_id = Column(String(32), ForeignKey("roles.id", onupdate="CASCADE"), primary_key=True)

    __table_args__ = (
        UniqueConstraint('id', name='uq_user_roles_id'),
    )
