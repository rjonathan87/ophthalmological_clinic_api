from app.data.repositories.clinical_protocol_repository import ClinicalProtocolRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List, Optional

class ClinicalProtocolService:
    def __init__(self, db: Session):
        self.repository = ClinicalProtocolRepository(db)

    def create_protocol(self, protocol: schemas.ClinicalProtocolCreate) -> schemas.ClinicalProtocolInDB:
        return self.repository.create(protocol)

    def get_protocol(self, protocol_id: int) -> Optional[schemas.ClinicalProtocolInDB]:
        return self.repository.get_by_id(protocol_id)

    def get_protocols(self, skip: int = 0, limit: int = 100) -> List[schemas.ClinicalProtocolInDB]:
        return self.repository.get_all(skip, limit)

    def update_protocol(self, protocol_id: int, protocol: schemas.ClinicalProtocolUpdate) -> Optional[schemas.ClinicalProtocolInDB]:
        return self.repository.update(protocol_id, protocol)

    def delete_protocol(self, protocol_id: int) -> bool:
        return self.repository.delete(protocol_id)
