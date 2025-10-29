from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import declared_attr
from nanoid import generate


class BaseMixin:
    PREFIX = ""
    SIZE = 26
    @classmethod
    def generate_id(cls):
        ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        return f"{cls.PREFIX}_{generate(alphabet=ALPHABET, size=cls.SIZE)}"
    
    @declared_attr
    def id(cls):
        return Column(String(32), primary_key=True, default=cls.generate_id)

    @declared_attr
    def created_at(cls):
        return Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    @declared_attr
    def updated_at(cls):
        return Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    @declared_attr
    def deleted_at(cls):
        return Column(TIMESTAMP, nullable=True)

    @declared_attr
    def deleted_by(cls):
        return Column(String(32), ForeignKey("users.id", onupdate="CASCADE", ondelete="SET NULL"), nullable=True)

    @declared_attr
    def created_by(cls):
        return Column(String(32), ForeignKey("users.id", onupdate="CASCADE", ondelete="SET NULL"), nullable=True)

    @declared_attr
    def updated_by(cls):
        return Column(String(32), ForeignKey("users.id", onupdate="CASCADE", ondelete="SET NULL"), nullable=True)