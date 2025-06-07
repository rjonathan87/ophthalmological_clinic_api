from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.domain import schemas
from app.services.resource_service import ResourceService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.ResourceInDB)
def create_resource(
    resource: schemas.ResourceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.gestionar_clinicas"))
):
    service = ResourceService(db)
    return service.create_resource(resource, current_user.id)

@router.get("/", response_model=List[schemas.ResourceInDB])
def get_resources(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = ResourceService(db)
    return service.get_resources(skip, limit)

@router.get("/{resource_id}", response_model=schemas.ResourceInDB)
def get_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = ResourceService(db)
    resource = service.get_resource(resource_id)
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.get("/clinic/{clinic_id}", response_model=List[schemas.ResourceInDB])
def get_clinic_resources(
    clinic_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = ResourceService(db)
    return service.get_clinic_resources(clinic_id)

@router.put("/{resource_id}", response_model=schemas.ResourceInDB)
def update_resource(
    resource_id: int,
    resource: schemas.ResourceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.gestionar_clinicas"))
):
    service = ResourceService(db)
    updated_resource = service.update_resource(resource_id, resource, current_user.id)
    if not updated_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return updated_resource

@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.gestionar_clinicas"))
):
    service = ResourceService(db)
    if not service.delete_resource(resource_id):
        raise HTTPException(status_code=404, detail="Resource not found")
    return None