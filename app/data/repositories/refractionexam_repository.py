from sqlalchemy.orm import Session
from app.domain import schemas
from typing import List, Optional
from datetime import datetime

from app.domain.models.refractionexam import RefractionExam

class RefractionExamRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, refractionexam: schemas.RefractionExamCreate, created_by_user_id: int) -> RefractionExam:
        db_refractionexam = RefractionExam(
            **refractionexam.dict(),
            created_by_user_id=created_by_user_id,
            updated_by_user_id=created_by_user_id
        )
        self.db.add(db_refractionexam)
        self.db.commit()
        self.db.refresh(db_refractionexam)
        return db_refractionexam

    def get_by_id(self, refractionexam_id: int) -> Optional[RefractionExam]:
        return self.db.query(RefractionExam).filter(
            RefractionExam.id == refractionexam_id,
            RefractionExam.deleted_at == None
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[RefractionExam]:
        return self.db.query(RefractionExam).filter(
            RefractionExam.deleted_at == None
        ).offset(skip).limit(limit).all()

    def get_by_consultation_id(self, consultation_id: int, skip: int = 0, limit: int = 100) -> List[RefractionExam]:
        return self.db.query(RefractionExam).filter(
            RefractionExam.consultation_id == consultation_id,
            RefractionExam.deleted_at == None
        ).offset(skip).limit(limit).all()

    def update(self, refractionexam_id: int, refractionexam: schemas.RefractionExamUpdate, updated_by_user_id: int) -> Optional[RefractionExam]:
        db_refractionexam = self.get_by_id(refractionexam_id)
        if db_refractionexam:
            update_data = refractionexam.dict(exclude_unset=True)
            update_data["updated_by_user_id"] = updated_by_user_id
            for key, value in update_data.items():
                setattr(db_refractionexam, key, value)
            self.db.commit()
            self.db.refresh(db_refractionexam)
        return db_refractionexam

    def soft_delete(self, refractionexam_id: int) -> bool:
        db_refractionexam = self.get_by_id(refractionexam_id)
        if db_refractionexam:
            db_refractionexam.deleted_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
