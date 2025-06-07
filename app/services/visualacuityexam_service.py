from app.data.repositories.visualacuityexam_repository import VisualAcuityExamRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status

class VisualAcuityExamService:
    def __init__(self, db: Session):
        self.repository = VisualAcuityExamRepository(db)

    def create_visualacuityexam(self, visualacuityexam: schemas.VisualAcuityExamCreate, created_by_user_id: int) -> schemas.VisualAcuityExamInDB:
        return self.repository.create(visualacuityexam, created_by_user_id)

    def get_visualacuityexam(self, visualacuityexam_id: int) -> Optional[schemas.VisualAcuityExamInDB]:
        visualacuityexam = self.repository.get_by_id(visualacuityexam_id)
        if not visualacuityexam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Visual acuity exam not found"
            )
        return visualacuityexam

    def get_visualacuityexams(self, skip: int = 0, limit: int = 100) -> List[schemas.VisualAcuityExamInDB]:
        return self.repository.get_all(skip, limit)

    def get_consultation_visualacuityexams(self, consultation_id: int, skip: int = 0, limit: int = 100) -> List[schemas.VisualAcuityExamInDB]:
        return self.repository.get_by_consultation_id(consultation_id, skip, limit)

    def update_visualacuityexam(self, visualacuityexam_id: int, visualacuityexam: schemas.VisualAcuityExamUpdate, updated_by_user_id: int) -> Optional[schemas.VisualAcuityExamInDB]:
        updated_visualacuityexam = self.repository.update(visualacuityexam_id, visualacuityexam, updated_by_user_id)
        if not updated_visualacuityexam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Visual acuity exam not found"
            )
        return updated_visualacuityexam

    def delete_visualacuityexam(self, visualacuityexam_id: int) -> bool:
        if not self.repository.soft_delete(visualacuityexam_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Visual acuity exam not found"
            )
        return True
