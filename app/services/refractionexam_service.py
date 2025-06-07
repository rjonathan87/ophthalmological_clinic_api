from app.data.repositories.refractionexam_repository import RefractionExamRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status

class RefractionExamService:
    def __init__(self, db: Session):
        self.repository = RefractionExamRepository(db)

    def create_refractionexam(self, refractionexam: schemas.RefractionExamCreate, created_by_user_id: int) -> schemas.RefractionExamInDB:
        return self.repository.create(refractionexam, created_by_user_id)

    def get_refractionexam(self, refractionexam_id: int) -> Optional[schemas.RefractionExamInDB]:
        refractionexam = self.repository.get_by_id(refractionexam_id)
        if not refractionexam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Refraction exam not found"
            )
        return refractionexam

    def get_refractionexams(self, skip: int = 0, limit: int = 100) -> List[schemas.RefractionExamInDB]:
        return self.repository.get_all(skip, limit)

    def get_consultation_refractionexams(self, consultation_id: int, skip: int = 0, limit: int = 100) -> List[schemas.RefractionExamInDB]:
        return self.repository.get_by_consultation_id(consultation_id, skip, limit)

    def update_refractionexam(self, refractionexam_id: int, refractionexam: schemas.RefractionExamUpdate, updated_by_user_id: int) -> Optional[schemas.RefractionExamInDB]:
        updated_refractionexam = self.repository.update(refractionexam_id, refractionexam, updated_by_user_id)
        if not updated_refractionexam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Refraction exam not found"
            )
        return updated_refractionexam

    def delete_refractionexam(self, refractionexam_id: int) -> bool:
        if not self.repository.soft_delete(refractionexam_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Refraction exam not found"
            )
        return True
