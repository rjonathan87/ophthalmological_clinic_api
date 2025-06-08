from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.models.patientdocument import PatientDocument
from app.domain.schemas import PatientDocumentCreate, PatientDocumentUpdate
from datetime import datetime
from sqlalchemy import or_

class PatientDocumentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, document: PatientDocumentCreate, created_by_user_id: int) -> PatientDocument:
        db_document = PatientDocument(**document.model_dump(), created_by_user_id=created_by_user_id)
        self.db.add(db_document)
        self.db.commit()
        self.db.refresh(db_document)
        return db_document

    def get_by_id(self, document_id: int) -> Optional[PatientDocument]:
        return self.db.query(PatientDocument).filter(
            PatientDocument.id == document_id,
            PatientDocument.deleted_at.is_(None)
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[PatientDocument]:
        return self.db.query(PatientDocument)\
            .filter(PatientDocument.deleted_at.is_(None))\
            .offset(skip)\
            .limit(limit)\
            .all()

    def get_by_patient_id(self, patient_id: int, skip: int = 0, limit: int = 100) -> List[PatientDocument]:
        return self.db.query(PatientDocument)\
            .filter(
                PatientDocument.patient_id == patient_id,
                PatientDocument.deleted_at.is_(None)
            )\
            .offset(skip)\
            .limit(limit)\
            .all()

    def get_by_clinic_id(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[PatientDocument]:
        return self.db.query(PatientDocument)\
            .filter(
                PatientDocument.clinic_id == clinic_id,
                PatientDocument.deleted_at.is_(None)
            )\
            .offset(skip)\
            .limit(limit)\
            .all()

    def search(self, search_term: str, clinic_id: int, skip: int = 0, limit: int = 100) -> List[PatientDocument]:
        return self.db.query(PatientDocument)\
            .filter(
                PatientDocument.clinic_id == clinic_id,
                PatientDocument.deleted_at.is_(None),
                or_(
                    PatientDocument.title.ilike(f"%{search_term}%"),
                    PatientDocument.document_type.ilike(f"%{search_term}%"),
                    PatientDocument.description.ilike(f"%{search_term}%")
                )
            )\
            .offset(skip)\
            .limit(limit)\
            .all()

    def update(self, document_id: int, document: PatientDocumentUpdate, updated_by_user_id: int) -> Optional[PatientDocument]:
        db_document = self.get_by_id(document_id)
        if db_document:
            update_data = document.model_dump(exclude_unset=True)
            update_data["updated_by_user_id"] = updated_by_user_id
            for key, value in update_data.items():
                setattr(db_document, key, value)
            self.db.commit()
            self.db.refresh(db_document)
        return db_document

    def delete(self, document_id: int) -> bool:
        db_document = self.get_by_id(document_id)
        if db_document:
            db_document.deleted_at = datetime.utcnow()
            self.db.commit()
            return True
        return False

    def hard_delete(self, document_id: int) -> bool:
        db_document = self.get_by_id(document_id)
        if db_document:
            self.db.delete(db_document)
            self.db.commit()
            return True
        return False
