from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.clinical_study_service import ClinicalStudyService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.ClinicalStudyInDB, status_code=status.HTTP_201_CREATED)
def create_clinical_study(
    study: schemas.ClinicalStudyCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.manage_clinical_studies"))
):
    service = ClinicalStudyService(db)
    return service.create_study(study)

@router.get("/", response_model=List[schemas.ClinicalStudyInDB])
def read_clinical_studies(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.manage_clinical_studies"))
):
    service = ClinicalStudyService(db)
    return service.get_studies(skip, limit)

@router.get("/{study_id}", response_model=schemas.ClinicalStudyInDB)
def read_clinical_study(
    study_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.manage_clinical_studies"))
):
    service = ClinicalStudyService(db)
    db_study = service.get_study(study_id)
    if db_study is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinical Study not found")
    return db_study

@router.put("/{study_id}", response_model=schemas.ClinicalStudyInDB)
def update_clinical_study(
    study_id: int,
    study: schemas.ClinicalStudyUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.manage_clinical_studies"))
):
    service = ClinicalStudyService(db)
    db_study = service.update_study(study_id, study)
    if db_study is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinical Study not found")
    return db_study

@router.delete("/{study_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clinical_study(
    study_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.manage_clinical_studies"))
):
    service = ClinicalStudyService(db)
    success = service.delete_study(study_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinical Study not found")
    return {"detail": "Clinical Study deleted successfully"}
