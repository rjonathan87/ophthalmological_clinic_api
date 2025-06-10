from app.data.repositories.lead_repository import LeadRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List, Optional

class LeadService:
    def __init__(self, db: Session):
        self.repository = LeadRepository(db)

    def create_lead(self, lead: schemas.LeadCreate) -> schemas.LeadInDB:
        """Crea un nuevo lead"""
        return self.repository.create(lead)

    def get_lead(self, lead_id: int) -> Optional[schemas.LeadInDB]:
        """Obtiene un lead por su ID"""
        return self.repository.get_by_id(lead_id)

    def get_lead_by_mobile_phone(self, mobile_phone: str) -> Optional[schemas.LeadInDB]:
        """Obtiene un lead por su número de teléfono móvil"""
        return self.repository.get_by_mobile_phone(mobile_phone)

    def get_lead_by_email(self, email: str) -> Optional[schemas.LeadInDB]:
        """Obtiene un lead por su email"""
        return self.repository.get_by_email(email)

    def get_leads(self, skip: int = 0, limit: int = 100) -> List[schemas.LeadInDB]:
        """Obtiene todos los leads con paginación"""
        return self.repository.get_all(skip, limit)

    def get_leads_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[schemas.LeadInDB]:
        """Obtiene leads por su estado"""
        return self.repository.get_by_status(status, skip, limit)

    def get_leads_by_service(self, service_id: int, skip: int = 0, limit: int = 100) -> List[schemas.LeadInDB]:
        """Obtiene leads por ID de servicio"""
        return self.repository.get_by_service_id(service_id, skip, limit)

    def get_leads_by_channel(self, channel: str, skip: int = 0, limit: int = 100) -> List[schemas.LeadInDB]:
        """Obtiene leads por canal"""
        return self.repository.get_by_channel(channel, skip, limit)

    def search_leads(self, query: str, skip: int = 0, limit: int = 100) -> List[schemas.LeadInDB]:
        """Busca leads por nombre, apellido, email o teléfono"""
        return self.repository.search(query, skip, limit)

    def update_lead(self, lead_id: int, lead: schemas.LeadUpdate) -> Optional[schemas.LeadInDB]:
        """Actualiza un lead existente por su ID"""
        return self.repository.update(lead_id, lead)

    def update_lead_status(self, lead_id: int, status_update: schemas.LeadStatusUpdate) -> Optional[schemas.LeadInDB]:
        """Actualiza solo el estado de un lead"""
        return self.repository.update_status(lead_id, status_update.status)

    def delete_lead(self, lead_id: int) -> bool:
        """Elimina un lead por su ID"""
        return self.repository.delete(lead_id)
