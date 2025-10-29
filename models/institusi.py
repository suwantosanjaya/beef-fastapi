from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from core.database import Base
from models.base_mixin import BaseMixin
from models.users import Users

class Institusi(BaseMixin, Base):
    __tablename__ = "institusi"
    PREFIX = "INSTI"

    nama_institusi = Column(String(100), unique=True, nullable=False)
    akronim = Column(String(255), unique=True, nullable=False)
    logo = Column(String(255), nullable=True)
    created_by = Column(String(32), ForeignKey("users.id", onupdate="CASCADE", ondelete="SET NULL"), nullable=True)
    updated_by = Column(String(32), ForeignKey("users.id", onupdate="CASCADE", ondelete="SET NULL"), nullable=True)
    deleted_by = Column(String(32), ForeignKey("users.id", onupdate="CASCADE", ondelete="SET NULL"), nullable=True)

    created_by_detail = relationship("Users", backref="institusi_created", foreign_keys=[created_by])
    updated_by_detail = relationship("Users", backref="institusi_updated", foreign_keys=[updated_by])
    deleted_by_detail = relationship("Users", backref="institusi_deleted", foreign_keys=[deleted_by])
   