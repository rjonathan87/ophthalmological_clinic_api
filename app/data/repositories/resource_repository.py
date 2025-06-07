from sqlalchemy.orm import Session
from app.domain import models, schemas
from typing import List, Optional
from datetime import datetime

class ResourceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, resource: schemas.ResourceCreate, user_id: int) -> models.Resource:
        db_resource = models.Resource(
            **resource.dict(),
            created_by_user_id=user_id
        )
        self.db.add(db_resource)
        self.db.commit()
        self.db.refresh(db_resource)
        return db_resource

    def get_by_id(self, resource_id: int) -> Optional[models.Resource]:
        return self.db.query(models.Resource).filter(
            models.Resource.id == resource_id,
            models.Resource.deleted_at.is_(None)
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[models.Resource]:
        return self.db.query(models.Resource).filter(
            models.Resource.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()

    def get_by_clinic(self, clinic_id: int) -> List[models.Resource]:
        return self.db.query(models.Resource).filter(
            models.Resource.clinic_id == clinic_id,
            models.Resource.deleted_at.is_(None)
        ).all()

    def update(self, resource_id: int, resource: schemas.ResourceUpdate, user_id: int) -> Optional[models.Resource]:
        db_resource = self.get_by_id(resource_id)
        if db_resource:
            update_data = resource.dict(exclude_unset=True)
            update_data["updated_by_user_id"] = user_id
            for key, value in update_data.items():
                setattr(db_resource, key, value)
            self.db.commit()
            self.db.refresh(db_resource)
        return db_resource

    def delete(self, resource_id: int) -> bool:
        db_resource = self.get_by_id(resource_id)
        if db_resource:
            db_resource.deleted_at = datetime.utcnow()
            self.db.commit()
            return True
        return False