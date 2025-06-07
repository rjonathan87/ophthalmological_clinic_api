from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.models.educationalresources import EducationalResource
from app.domain.schemas import EducationalResourceCreate, EducationalResourceUpdate

class EducationalResourceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, resource: EducationalResourceCreate) -> EducationalResource:
        db_resource = EducationalResource(**resource.model_dump())
        self.db.add(db_resource)
        self.db.commit()
        self.db.refresh(db_resource)
        return db_resource

    def get_by_id(self, resource_id: int) -> Optional[EducationalResource]:
        return self.db.query(EducationalResource).filter(EducationalResource.id == resource_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[EducationalResource]:
        return self.db.query(EducationalResource).offset(skip).limit(limit).all()

    def update(self, resource_id: int, resource: EducationalResourceUpdate) -> Optional[EducationalResource]:
        db_resource = self.get_by_id(resource_id)
        if db_resource:
            update_data = resource.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_resource, field, value)
            self.db.commit()
            self.db.refresh(db_resource)
        return db_resource

    def delete(self, resource_id: int) -> bool:
        db_resource = self.get_by_id(resource_id)
        if db_resource:
            self.db.delete(db_resource)
            self.db.commit()
            return True
        return False