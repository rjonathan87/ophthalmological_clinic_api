from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.refractionexam_service import RefractionExamService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.RefractionExamResponse)
def create_refractionexam(
    refractionexam: schemas.RefractionExamCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("refraccion.crear"))
):
    service = RefractionExamService(db)
    return service.create_refractionexam(refractionexam, current_user.id)

@router.get("/", response_model=List[schemas.RefractionExamResponse])
def get_refractionexams(
    consultation_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("refraccion.ver"))
):
    service = RefractionExamService(db)
    if consultation_id:
        return service.get_consultation_refractionexams(consultation_id, skip, limit)
    return service.get_refractionexams(skip, limit)

@router.get("/{refractionexam_id}", response_model=schemas.RefractionExamResponse)
def get_refractionexam(
    refractionexam_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("refraccion.ver"))
):
    service = RefractionExamService(db)
    return service.get_refractionexam(refractionexam_id)

@router.put("/{refractionexam_id}", response_model=schemas.RefractionExamResponse)
def update_refractionexam(
    refractionexam_id: int,
    refractionexam: schemas.RefractionExamUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("refraccion.editar"))
):
    service = RefractionExamService(db)
    return service.update_refractionexam(refractionexam_id, refractionexam, current_user.id)

@router.delete("/{refractionexam_id}")
def delete_refractionexam(
    refractionexam_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("refraccion.eliminar"))
):
    service = RefractionExamService(db)
    return service.delete_refractionexam(refractionexam_id)
