from sqlalchemy.orm import Session
from app.domain import schemas
from typing import List, Optional
from datetime import datetime

from app.domain.models.visualacuityexam import VisualAcuityExam

class VisualAcuityExamRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, visualacuityexam: schemas.VisualAcuityExamCreate, created_by_user_id: int) -> VisualAcuityExam:
        db_visualacuityexam = VisualAcuityExam(
            **visualacuityexam.dict(),
            created_by_user_id=created_by_user_id,
            updated_by_user_id=created_by_user_id
        )
        self.db.add(db_visualacuityexam)
        self.db.commit()
        self.db.refresh(db_visualacuityexam)
        return db_visualacuityexam

    def get_by_id(self, visualacuityexam_id: int) -> Optional[VisualAcuityExam]:
        return self.db.query(VisualAcuityExam).filter(
            VisualAcuityExam.id == visualacuityexam_id,
            VisualAcuityExam.deleted_at == None
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[VisualAcuityExam]:
        return self.db.query(VisualAcuityExam).filter(
            VisualAcuityExam.deleted_at == None
        ).offset(skip).limit(limit).all()

    def get_by_consultation_id(self, consultation_id: int, skip: int = 0, limit: int = 100) -> List[VisualAcuityExam]:
        return self.db.query(VisualAcuityExam).filter(
            VisualAcuityExam.consultation_id == consultation_id,
            VisualAcuityExam.deleted_at == None
        ).offset(skip).limit(limit).all()

    def update(self, visualacuityexam_id: int, visualacuityexam: schemas.VisualAcuityExamUpdate, updated_by_user_id: int) -> Optional[VisualAcuityExam]:
        db_visualacuityexam = self.get_by_id(visualacuityexam_id)
        if db_visualacuityexam:
            update_data = visualacuityexam.dict(exclude_unset=True)
            update_data["updated_by_user_id"] = updated_by_user_id
            for key, value in update_data.items():
                setattr(db_visualacuityexam, key, value)
            self.db.commit()
            self.db.refresh(db_visualacuityexam)
        return db_visualacuityexam

    def soft_delete(self, visualacuityexam_id: int) -> bool:
        db_visualacuityexam = self.get_by_id(visualacuityexam_id)
        if db_visualacuityexam:
            db_visualacuityexam.deleted_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
