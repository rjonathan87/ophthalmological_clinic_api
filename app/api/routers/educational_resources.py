from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.domain.schemas import (
    EducationalResourceCreate,
    EducationalResourceUpdate,
    EducationalResourceInDB
)
from app.services.educational_resource_service import EducationalResourceService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter(
    tags=["Educational Resources"]
)

@router.post("/", response_model=EducationalResourceInDB)
def create_educational_resource(
    resource: EducationalResourceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.gestionar_recursos_educativos"))
):
    service = EducationalResourceService(db)
    return service.create_resource(resource)

@router.get("/", response_model=List[EducationalResourceInDB])
def get_educational_resources(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = EducationalResourceService(db)
    return service.get_resources(skip, limit)

@router.get("/{resource_id}", response_model=EducationalResourceInDB)
def get_educational_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = EducationalResourceService(db)
    resource = service.get_resource(resource_id)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Educational resource not found"
        )
    return resource

@router.put("/{resource_id}", response_model=EducationalResourceInDB)
def update_educational_resource(
    resource_id: int,
    resource: EducationalResourceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.gestionar_recursos_educativos"))
):
    service = EducationalResourceService(db)
    updated_resource = service.update_resource(resource_id, resource)
    if not updated_resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Educational resource not found"
        )
    return updated_resource

@router.delete("/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_educational_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.gestionar_recursos_educativos"))
):
    service = EducationalResourceService(db)
    if not service.delete_resource(resource_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Educational resource not found"
        )