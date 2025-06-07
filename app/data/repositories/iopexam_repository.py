from sqlalchemy.orm import Session
from app.domain import schemas, models
from typing import List, Optional
from datetime import datetime

class IOPExamRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, iopexam: schemas.IOPExamCreate, created_by_user_id: int) -> models.IOPExam:
        db_iopexam = models.IOPExam(
            **iopexam.dict(),
            created_by_user_id=created_by_user_id,
            updated_by_user_id=created_by_user_id
        )
        self.db.add(db_iopexam)
        self.db.commit()
        self.db.refresh(db_iopexam)
        return db_iopexam

    def get_by_id(self, iopexam_id: int) -> Optional[models.IOPExam]:
        return self.db.query(models.IOPExam).filter(
            models.IOPExam.id == iopexam_id,
            models.IOPExam.deleted_at == None
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[models.IOPExam]:
        return self.db.query(models.IOPExam).filter(
            models.IOPExam.deleted_at == None
        ).offset(skip).limit(limit).all()

    def get_by_consultation_id(self, consultation_id: int, skip: int = 0, limit: int = 100) -> List[models.IOPExam]:
        return self.db.query(models.IOPExam).filter(
            models.IOPExam.consultation_id == consultation_id,
            models.IOPExam.deleted_at == None
        ).offset(skip).limit(limit).all()

    def update(self, iopexam_id: int, iopexam: schemas.IOPExamUpdate, updated_by_user_id: int) -> Optional[models.IOPExam]:
        db_iopexam = self.get_by_id(iopexam_id)
        if db_iopexam:
            update_data = iopexam.dict(exclude_unset=True)
            update_data["updated_by_user_id"] = updated_by_user_id
            for key, value in update_data.items():
                setattr(db_iopexam, key, value)
            self.db.commit()
            self.db.refresh(db_iopexam)
        return db_iopexam

    def soft_delete(self, iopexam_id: int) -> bool:
        db_iopexam = self.get_by_id(iopexam_id)
        if db_iopexam:
            db_iopexam.deleted_at = datetime.utcnow()
            self.db.commit()
            return True
        return False
