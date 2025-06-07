from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.visualacuityexam_service import VisualAcuityExamService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.VisualAcuityExamResponse)
def create_visualacuityexam(
    visualacuityexam: schemas.VisualAcuityExamCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("agudeza_visual.crear"))
):
    service = VisualAcuityExamService(db)
    return service.create_visualacuityexam(visualacuityexam, current_user.id)

@router.get("/", response_model=List[schemas.VisualAcuityExamResponse])
def get_visualacuityexams(
    consultation_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("agudeza_visual.ver"))
):
    service = VisualAcuityExamService(db)
    if consultation_id:
        return service.get_consultation_visualacuityexams(consultation_id, skip, limit)
    return service.get_visualacuityexams(skip, limit)

@router.get("/{visualacuityexam_id}", response_model=schemas.VisualAcuityExamResponse)
def get_visualacuityexam(
    visualacuityexam_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("agudeza_visual.ver"))
):
    service = VisualAcuityExamService(db)
    return service.get_visualacuityexam(visualacuityexam_id)

@router.put("/{visualacuityexam_id}", response_model=schemas.VisualAcuityExamResponse)
def update_visualacuityexam(
    visualacuityexam_id: int,
    visualacuityexam: schemas.VisualAcuityExamUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("agudeza_visual.editar"))
):
    service = VisualAcuityExamService(db)
    return service.update_visualacuityexam(visualacuityexam_id, visualacuityexam, current_user.id)

@router.delete("/{visualacuityexam_id}")
def delete_visualacuityexam(
    visualacuityexam_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("agudeza_visual.eliminar"))
):
    service = VisualAcuityExamService(db)
    return service.delete_visualacuityexam(visualacuityexam_id)
