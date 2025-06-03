from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.clinical_protocol_service import ClinicalProtocolService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.ClinicalProtocolInDB, status_code=status.HTTP_201_CREATED)
def create_clinical_protocol(
    protocol: schemas.ClinicalProtocolCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.manage_clinical_protocols"))
):
    service = ClinicalProtocolService(db)
    return service.create_protocol(protocol)

@router.get("/", response_model=List[schemas.ClinicalProtocolInDB])
def read_clinical_protocols(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.manage_clinical_protocols"))
):
    service = ClinicalProtocolService(db)
    return service.get_protocols(skip, limit)

@router.get("/{protocol_id}", response_model=schemas.ClinicalProtocolInDB)
def read_clinical_protocol(
    protocol_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.manage_clinical_protocols"))
):
    service = ClinicalProtocolService(db)
    db_protocol = service.get_protocol(protocol_id)
    if db_protocol is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinical Protocol not found")
    return db_protocol

@router.put("/{protocol_id}", response_model=schemas.ClinicalProtocolInDB)
def update_clinical_protocol(
    protocol_id: int,
    protocol: schemas.ClinicalProtocolUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.manage_clinical_protocols"))
):
    service = ClinicalProtocolService(db)
    db_protocol = service.update_protocol(protocol_id, protocol)
    if db_protocol is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinical Protocol not found")
    return db_protocol

@router.delete("/{protocol_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_clinical_protocol(
    protocol_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.manage_clinical_protocols"))
):
    service = ClinicalProtocolService(db)
    success = service.delete_protocol(protocol_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Clinical Protocol not found")
    return {"detail": "Clinical Protocol deleted successfully"}
