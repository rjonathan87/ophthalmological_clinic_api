from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.domain import schemas
from app.services.service_service import ServiceService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.ServiceResponse)
def create_service(
    service: schemas.ServiceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("services.create"))
):
    """
    Create a new service.
    Requires the services.create permission.
    """
    service_service = ServiceService(db)
    return service_service.create_service(service, current_user.id)

@router.get("/clinic/{clinic_id}", response_model=List[schemas.ServiceResponse])
def get_clinic_services(
    clinic_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("services.read"))
):
    """
    Get all services for a specific clinic.
    Requires the services.read permission.
    """
    service_service = ServiceService(db)
    return service_service.get_clinic_services(clinic_id, skip=skip, limit=limit)

@router.get("/{service_id}", response_model=schemas.ServiceResponse)
def get_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("services.read"))
):
    """
    Get a specific service by ID.
    Requires the services.read permission.
    """
    service_service = ServiceService(db)
    return service_service.get_service(service_id)

@router.put("/{service_id}", response_model=schemas.ServiceResponse)
def update_service(
    service_id: int,
    service: schemas.ServiceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("services.update"))
):
    """
    Update a service.
    Requires the services.update permission.
    """
    service_service = ServiceService(db)
    return service_service.update_service(service_id, service, current_user.id)

@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(
    service_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("services.delete"))
):
    """
    Delete a service.
    Requires the services.delete permission.
    """
    service_service = ServiceService(db)
    if not service_service.delete_service(service_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service with id {service_id} not found"
        )
