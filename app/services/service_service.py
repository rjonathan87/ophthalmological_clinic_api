from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.data.repositories.service_repository import ServiceRepository
from app.domain import schemas
from typing import List, Optional

class ServiceService:
    def __init__(self, db: Session):
        self.repository = ServiceRepository(db)

    def create_service(self, service: schemas.ServiceCreate, user_id: int) -> schemas.ServiceInDB:
        if self.repository.check_service_exists(service.clinic_id, service.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service with name '{service.name}' already exists in this clinic"
            )
        return self.repository.create(service, user_id)

    def get_service(self, service_id: int, clinic_id: Optional[int] = None) -> schemas.ServiceInDB:
        db_service = self.repository.get_by_id(service_id, clinic_id)
        if not db_service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Service with id {service_id} not found"
            )
        return db_service    
    
    def get_clinic_services(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[schemas.ServiceInDB]:
        return self.repository.get_by_clinic(clinic_id, skip, limit)
        
    def get_services(self, skip: int = 0, limit: int = 100) -> List[schemas.ServiceInDB]:
        """
        Obtiene todos los servicios activos, independientemente de la clínica.
        Útil para listar servicios disponibles para leads/bots.
        """
        return self.repository.get_all_active(skip, limit)

    def update_service(self, service_id: int, service: schemas.ServiceUpdate, user_id: int) -> schemas.ServiceInDB:
        db_service = self.repository.get_by_id(service_id)
        if not db_service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Service with id {service_id} not found"
            )

        # Check if name is being updated and if it already exists
        if service.name and service.name != db_service.name:
            if self.repository.check_service_exists(service.clinic_id or db_service.clinic_id, service.name):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Service with name '{service.name}' already exists in this clinic"
                )

        updated_service = self.repository.update(service_id, service, user_id)
        return updated_service

    def delete_service(self, service_id: int, user_id: int) -> bool:
        db_service = self.repository.get_by_id(service_id)
        if not db_service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Service with id {service_id} not found"
            )
        return self.repository.delete(service_id, user_id)
