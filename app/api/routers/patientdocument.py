from fastapi import APIRouter, Depends, UploadFile, File, Query
from typing import List
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.domain.schemas import PatientDocumentCreate, PatientDocumentUpdate, PatientDocumentInDB, PatientDocumentResponse
from app.services.patientdocument_service import PatientDocumentService
from app.api.dependencies import get_current_user, require_permission
from app.domain.schemas import UserInDB

router = APIRouter()

@router.post("/", response_model=PatientDocumentResponse)
async def create_patient_document(
    document: PatientDocumentCreate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("documento.crear"))
):
    service = PatientDocumentService(db)
    return service.create_document(document, current_user.id)

@router.get("/{document_id}", response_model=PatientDocumentResponse)
async def get_patient_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("documento.ver"))
):
    service = PatientDocumentService(db)
    return service.get_document(document_id)

@router.get("/patient/{patient_id}", response_model=List[PatientDocumentResponse])
async def get_patient_documents(
    patient_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("documento.ver"))
):
    service = PatientDocumentService(db)
    return service.get_patient_documents(patient_id, skip, limit)

@router.get("/clinic/{clinic_id}", response_model=List[PatientDocumentResponse])
async def get_clinic_documents(
    clinic_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("documento.ver"))
):
    service = PatientDocumentService(db)
    return service.get_clinic_documents(clinic_id, skip, limit)

@router.get("/search/{clinic_id}", response_model=List[PatientDocumentResponse])
async def search_documents(
    clinic_id: int,
    search_term: str = Query(..., min_length=2),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("documento.ver"))
):
    service = PatientDocumentService(db)
    return service.search_documents(search_term, clinic_id, skip, limit)

@router.put("/{document_id}", response_model=PatientDocumentResponse)
async def update_patient_document(
    document_id: int,
    document: PatientDocumentUpdate,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("documento.editar"))
):
    service = PatientDocumentService(db)
    return service.update_document(document_id, document, current_user.id)

@router.delete("/{document_id}")
async def delete_patient_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: UserInDB = Depends(require_permission("documento.eliminar"))
):
    service = PatientDocumentService(db)
    return service.delete_document(document_id)
