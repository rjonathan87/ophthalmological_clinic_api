from sqlalchemy.orm import Session
from app.domain import models, schemas
from sqlalchemy import or_, and_
from typing import List, Optional

class LeadRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, lead: schemas.LeadCreate) -> models.Lead:
        """Crea un nuevo lead en la base de datos"""
        lead_data = lead.dict()
        
        # Corregir casos específicos
        if lead_data.get("service_id") == 0:
            lead_data["service_id"] = None
            
        db_lead = models.Lead(**lead_data)
        self.db.add(db_lead)
        self.db.commit()
        self.db.refresh(db_lead)
        return db_lead

    def get_by_id(self, lead_id: int) -> Optional[models.Lead]:
        """Obtiene un lead por su ID"""
        return self.db.query(models.Lead).filter(models.Lead.lead_id == lead_id).first()

    def get_by_mobile_phone(self, mobile_phone: str) -> Optional[models.Lead]:
        """Obtiene un lead por su número de teléfono móvil"""
        return self.db.query(models.Lead).filter(models.Lead.mobile_phone == mobile_phone).first()
    
    def get_by_email(self, email: str) -> Optional[models.Lead]:
        """Obtiene un lead por su email"""
        return self.db.query(models.Lead).filter(models.Lead.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[models.Lead]:
        """Obtiene todos los leads con paginación"""
        return self.db.query(models.Lead).offset(skip).limit(limit).all()

    def get_by_status(self, status: str, skip: int = 0, limit: int = 100) -> List[models.Lead]:
        """Obtiene leads por su estado"""
        return self.db.query(models.Lead).filter(models.Lead.status == status).offset(skip).limit(limit).all()

    def get_by_service_id(self, service_id: int, skip: int = 0, limit: int = 100) -> List[models.Lead]:
        """Obtiene leads por ID de servicio"""
        return self.db.query(models.Lead).filter(models.Lead.service_id == service_id).offset(skip).limit(limit).all()

    def get_by_channel(self, channel: str, skip: int = 0, limit: int = 100) -> List[models.Lead]:
        """Obtiene leads por canal"""
        return self.db.query(models.Lead).filter(models.Lead.channel == channel).offset(skip).limit(limit).all()

    def search(self, query: str, skip: int = 0, limit: int = 100) -> List[models.Lead]:
        """Busca leads por nombre, apellido, email o teléfono"""
        search_query = f"%{query}%"
        return self.db.query(models.Lead).filter(
            or_(
                models.Lead.first_name.ilike(search_query),
                models.Lead.last_name.ilike(search_query),
                models.Lead.email.ilike(search_query),
                models.Lead.mobile_phone.ilike(search_query)
            )
        ).offset(skip).limit(limit).all()

    def update(self, lead_id: int, lead: schemas.LeadUpdate) -> Optional[models.Lead]:
        """Actualiza un lead existente por su ID"""
        db_lead = self.get_by_id(lead_id)
        if db_lead:
            # Solo actualiza los campos no nulos
            update_data = lead.dict(exclude_unset=True)
            
            # Corregir casos específicos
            if "service_id" in update_data and (update_data["service_id"] == 0 or update_data["service_id"] is None):
                update_data["service_id"] = None
                
            if "appointment_id" in update_data and update_data["appointment_id"] == 0:
                update_data["appointment_id"] = None
                
            for key, value in update_data.items():
                setattr(db_lead, key, value)
                
            self.db.commit()
            self.db.refresh(db_lead)
        return db_lead

    def update_status(self, lead_id: int, status: str) -> Optional[models.Lead]:
        """Actualiza solo el estado de un lead"""
        db_lead = self.get_by_id(lead_id)
        if db_lead:
            db_lead.status = status
            self.db.commit()
            self.db.refresh(db_lead)
        return db_lead

    def delete(self, lead_id: int) -> bool:
        """Elimina un lead por su ID"""
        db_lead = self.get_by_id(lead_id)
        if db_lead:
            self.db.delete(db_lead)
            self.db.commit()
            return True
        return False
