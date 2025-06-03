from sqlalchemy.orm import Session
from app.domain import models, schemas
from typing import List, Optional

class ClinicalProtocolRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, protocol: schemas.ClinicalProtocolCreate) -> models.ClinicalProtocol:
        db_protocol = models.ClinicalProtocol(**protocol.model_dump())
        self.db.add(db_protocol)
        self.db.commit()
        self.db.refresh(db_protocol)
        return db_protocol

    def get_by_id(self, protocol_id: int) -> Optional[models.ClinicalProtocol]:
        return self.db.query(models.ClinicalProtocol).filter(models.ClinicalProtocol.id == protocol_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[models.ClinicalProtocol]:
        return self.db.query(models.ClinicalProtocol).offset(skip).limit(limit).all()

    def update(self, protocol_id: int, protocol: schemas.ClinicalProtocolUpdate) -> Optional[models.ClinicalProtocol]:
        db_protocol = self.get_by_id(protocol_id)
        if db_protocol:
            update_data = protocol.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_protocol, key, value)
            self.db.commit()
            self.db.refresh(db_protocol)
        return db_protocol

    def delete(self, protocol_id: int) -> bool:
        db_protocol = self.get_by_id(protocol_id)
        if db_protocol:
            self.db.delete(db_protocol)
            self.db.commit()
            return True
        return False
