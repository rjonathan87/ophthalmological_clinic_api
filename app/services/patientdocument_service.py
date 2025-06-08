from fastapi import HTTPException
from app.data.repositories.patientdocument_repository import PatientDocumentRepository
from app.domain.schemas import PatientDocumentCreate, PatientDocumentUpdate, PatientDocumentInDB
from sqlalchemy.orm import Session
from typing import List, Optional

class PatientDocumentService:
    def __init__(self, db: Session):
        self.repository = PatientDocumentRepository(db)

    def create_document(self, document: PatientDocumentCreate, created_by_user_id: int) -> PatientDocumentInDB:
        return self.repository.create(document, created_by_user_id)

    def get_document(self, document_id: int) -> Optional[PatientDocumentInDB]:
        document = self.repository.get_by_id(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        return document

    def get_documents(self, skip: int = 0, limit: int = 100) -> List[PatientDocumentInDB]:
        return self.repository.get_all(skip, limit)

    def get_patient_documents(self, patient_id: int, skip: int = 0, limit: int = 100) -> List[PatientDocumentInDB]:
        return self.repository.get_by_patient_id(patient_id, skip, limit)

    def get_clinic_documents(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[PatientDocumentInDB]:
        return self.repository.get_by_clinic_id(clinic_id, skip, limit)

    def search_documents(self, search_term: str, clinic_id: int, skip: int = 0, limit: int = 100) -> List[PatientDocumentInDB]:
        return self.repository.search(search_term, clinic_id, skip, limit)

    def update_document(self, document_id: int, document: PatientDocumentUpdate, updated_by_user_id: int) -> PatientDocumentInDB:
        updated_document = self.repository.update(document_id, document, updated_by_user_id)
        if not updated_document:
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        return updated_document

    def delete_document(self, document_id: int) -> bool:
        if not self.repository.delete(document_id):
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        return True

    def hard_delete_document(self, document_id: int) -> bool:
        if not self.repository.hard_delete(document_id):
            raise HTTPException(status_code=404, detail="Documento no encontrado")
        return True
