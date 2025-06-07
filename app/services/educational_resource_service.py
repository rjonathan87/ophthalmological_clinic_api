from typing import List, Optional
from sqlalchemy.orm import Session
from app.data.repositories.educational_resource_repository import EducationalResourceRepository
from app.domain.schemas import (
    EducationalResourceCreate,
    EducationalResourceUpdate,
    EducationalResourceInDB
)

class EducationalResourceService:
    def __init__(self, db: Session):
        self.repository = EducationalResourceRepository(db)

    def create_resource(self, resource: EducationalResourceCreate) -> EducationalResourceInDB:
        return self.repository.create(resource)

    def get_resource(self, resource_id: int) -> Optional[EducationalResourceInDB]:
        return self.repository.get_by_id(resource_id)

    def get_resources(self, skip: int = 0, limit: int = 100) -> List[EducationalResourceInDB]:
        return self.repository.get_all(skip, limit)

    def update_resource(self, resource_id: int, resource: EducationalResourceUpdate) -> Optional[EducationalResourceInDB]:
        return self.repository.update(resource_id, resource)

    def delete_resource(self, resource_id: int) -> bool:
        return self.repository.delete(resource_id)