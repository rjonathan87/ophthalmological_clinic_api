from app.data.repositories.iopexam_repository import IOPExamRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status

class IOPExamService:
    def __init__(self, db: Session):
        self.repository = IOPExamRepository(db)

    def create_iopexam(self, iopexam: schemas.IOPExamCreate, created_by_user_id: int) -> schemas.IOPExamInDB:
        return self.repository.create(iopexam, created_by_user_id)

    def get_iopexam(self, iopexam_id: int) -> Optional[schemas.IOPExamInDB]:
        iopexam = self.repository.get_by_id(iopexam_id)
        if not iopexam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="IOP exam not found"
            )
        return iopexam

    def get_iopexams(self, skip: int = 0, limit: int = 100) -> List[schemas.IOPExamInDB]:
        return self.repository.get_all(skip, limit)

    def get_consultation_iopexams(self, consultation_id: int, skip: int = 0, limit: int = 100) -> List[schemas.IOPExamInDB]:
        return self.repository.get_by_consultation_id(consultation_id, skip, limit)

    def update_iopexam(self, iopexam_id: int, iopexam: schemas.IOPExamUpdate, updated_by_user_id: int) -> Optional[schemas.IOPExamInDB]:
        updated_iopexam = self.repository.update(iopexam_id, iopexam, updated_by_user_id)
        if not updated_iopexam:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="IOP exam not found"
            )
        return updated_iopexam

    def delete_iopexam(self, iopexam_id: int) -> bool:
        if not self.repository.soft_delete(iopexam_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="IOP exam not found"
            )
        return True
