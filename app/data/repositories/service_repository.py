from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.domain.models.service import Service
from app.domain import schemas
from datetime import datetime
from typing import List, Optional

class ServiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, service: schemas.ServiceCreate, user_id: int) -> Service:
        db_service = Service(**service.model_dump())
        db_service.created_by_user_id = user_id
        db_service.updated_by_user_id = user_id
        self.db.add(db_service)
        self.db.commit()
        self.db.refresh(db_service)
        return db_service

    def get_by_id(self, service_id: int, clinic_id: Optional[int] = None) -> Optional[Service]:
        query = self.db.query(Service).filter(Service.id == service_id, Service.deleted_at == None)
        if clinic_id:
            query = query.filter(Service.clinic_id == clinic_id)
        return query.first()    
    
    def get_by_clinic(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[Service]:
        return self.db.query(Service).filter(
            and_(
                Service.clinic_id == clinic_id,
                Service.deleted_at == None
            )
        ).offset(skip).limit(limit).all()
        
    def get_all_active(self, skip: int = 0, limit: int = 100) -> List[Service]:
        """
        Obtiene todos los servicios activos de todas las clínicas.
        """
        return self.db.query(Service).filter(
            and_(
                Service.is_active == True,
                Service.deleted_at == None
            )
        ).offset(skip).limit(limit).all()

    def update(self, service_id: int, service: schemas.ServiceUpdate, user_id: int) -> Optional[Service]:
        db_service = self.get_by_id(service_id)
        if db_service:
            update_data = service.model_dump(exclude_unset=True)
            update_data['updated_by_user_id'] = user_id
            for key, value in update_data.items():
                setattr(db_service, key, value)
            self.db.commit()
            self.db.refresh(db_service)
        return db_service

    def delete(self, service_id: int, user_id: int) -> bool:
        db_service = self.get_by_id(service_id)
        if db_service:
            db_service.deleted_at = datetime.utcnow()
            db_service.updated_by_user_id = user_id
            self.db.commit()
            return True
        return False

    def check_service_exists(self, clinic_id: int, name: str) -> bool:
        return self.db.query(Service).filter(
            and_(
                Service.clinic_id == clinic_id,
                Service.name == name,
                Service.deleted_at == None
            )
        ).first() is not None
