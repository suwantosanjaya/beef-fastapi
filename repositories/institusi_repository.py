from datetime import datetime
from sqlalchemy.orm import Session
from core.database import get_db
from models.institusi import Institusi

class InstitusiRepository:
    def __init__(self, db: Session = None):
        self.db = db

    def get_all(self):
        return self.db.query(Institusi).order_by(Institusi.created_at.desc()).all()
    def get_all_active(self):
        return self.db.query(Institusi).filter(Institusi.deleted_at.is_(None)).order_by(Institusi.created_at.desc()).all()
    def get_all_ontrash(self):
        return self.db.query(Institusi).filter(Institusi.deleted_at.isnot(None)).order_by(Institusi.created_at.desc()).all()
    def get_by_id(self, id: str):
        return self.db.query(Institusi).filter(Institusi.id == id).first()
    def get_active_by_id(self, id: str):
        return self.db.query(Institusi).filter(Institusi.id == id, Institusi.deleted_at.is_(None)).first()
    def get_from_trash_by_id(self, id: str):
        return self.db.query(Institusi).filter(Institusi.id == id, Institusi.deleted_at.isnot(None)).first()
    def get_logo_by_id(self, id: str):
        return self.db.query(Institusi.logo).filter(Institusi.id == id).first()
    def get_active_by_ids(self, ids: list[str]):
        return self.db.query(Institusi).filter(Institusi.id.in_(ids), Institusi.deleted_at.is_(None)).all()
    def get_from_trash_by_ids(self, ids: list[str]):
        return self.db.query(Institusi).filter(Institusi.id.in_(ids), Institusi.deleted_at.isnot(None)).all()
    def add(self, institusi: Institusi):
        self.db.add(institusi)
        return institusi
    
    def update(self, institusi: Institusi, new_data: dict, user_id: str = None, new_logo: str = None):
        id = institusi.id
        for key, value in new_data.items():
            setattr(institusi, key, value)
        institusi.id = id
        institusi.updated_by = user_id if user_id else institusi.updated_by
        institusi.logo = new_logo if new_logo else institusi.logo
        return institusi
    
    def soft_delete(self, institusi: Institusi, user_id: str = None):
        institusi.deleted_at = datetime.now()
        institusi.deleted_by = user_id if user_id else institusi.deleted_by
        return institusi
    
    def restore(self, institusi: Institusi, user_id: str = None):
        institusi.deleted_at = None
        institusi.deleted_by = None
        return institusi
    
    def delete(self, institusi: Institusi, user_id: str = None):
        self.db.delete(institusi)
        return institusi