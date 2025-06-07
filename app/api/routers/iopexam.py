from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.iopexam_service import IOPExamService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.IOPExamResponse)
def create_iopexam(
    iopexam: schemas.IOPExamCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("iopexam.crear"))
):
    service = IOPExamService(db)
    return service.create_iopexam(iopexam, current_user.id)

@router.get("/", response_model=List[schemas.IOPExamResponse])
def get_iopexams(
    consultation_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("iopexam.ver"))
):
    service = IOPExamService(db)
    if consultation_id:
        return service.get_consultation_iopexams(consultation_id, skip, limit)
    return service.get_iopexams(skip, limit)

@router.get("/{iopexam_id}", response_model=schemas.IOPExamResponse)
def get_iopexam(
    iopexam_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("iopexam.ver"))
):
    service = IOPExamService(db)
    return service.get_iopexam(iopexam_id)

@router.put("/{iopexam_id}", response_model=schemas.IOPExamResponse)
def update_iopexam(
    iopexam_id: int,
    iopexam: schemas.IOPExamUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("iopexam.editar"))
):
    service = IOPExamService(db)
    return service.update_iopexam(iopexam_id, iopexam, current_user.id)

@router.delete("/{iopexam_id}")
def delete_iopexam(
    iopexam_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("iopexam.eliminar"))
):
    service = IOPExamService(db)
    return service.delete_iopexam(iopexam_id)
