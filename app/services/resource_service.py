from app.data.repositories.resource_repository import ResourceRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List, Optional

class ResourceService:
    def __init__(self, db: Session):
        self.repository = ResourceRepository(db)

    def create_resource(self, resource: schemas.ResourceCreate, user_id: int) -> schemas.ResourceInDB:
        return self.repository.create(resource, user_id)

    def get_resource(self, resource_id: int) -> Optional[schemas.ResourceInDB]:
        return self.repository.get_by_id(resource_id)

    def get_resources(self, skip: int = 0, limit: int = 100) -> List[schemas.ResourceInDB]:
        return self.repository.get_all(skip, limit)

    def get_clinic_resources(self, clinic_id: int) -> List[schemas.ResourceInDB]:
        return self.repository.get_by_clinic(clinic_id)

    def update_resource(self, resource_id: int, resource: schemas.ResourceUpdate, user_id: int) -> Optional[schemas.ResourceInDB]:
        return self.repository.update(resource_id, resource, user_id)

    def delete_resource(self, resource_id: int) -> bool:
        return self.repository.delete(resource_id)