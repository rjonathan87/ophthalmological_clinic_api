from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.invoice_service import InvoiceService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.InvoiceResponse, status_code=status.HTTP_201_CREATED)
def create_invoice(
    invoice: schemas.InvoiceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("factura.crear"))
):
    service = InvoiceService(db)
    return service.create_invoice(invoice, current_user.id)

@router.get("/", response_model=List[schemas.InvoiceResponse])
def get_invoices(
    patient_id: Optional[int] = None,
    clinic_id: Optional[int] = None,
    consultation_id: Optional[int] = None,
    appointment_id: Optional[int] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("factura.ver"))
):
    service = InvoiceService(db)
    
    if search:
        return service.search_invoices(search, clinic_id)
    elif patient_id:
        return service.get_patient_invoices(patient_id, skip, limit)
    elif clinic_id:
        return service.get_clinic_invoices(clinic_id, skip, limit)
    elif consultation_id:
        return service.get_consultation_invoices(consultation_id, skip, limit)
    elif appointment_id:
        return service.get_appointment_invoices(appointment_id, skip, limit)
    return service.get_invoices(skip, limit)

@router.get("/{invoice_id}", response_model=schemas.InvoiceResponse)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("factura.ver"))
):
    service = InvoiceService(db)
    return service.get_invoice(invoice_id)

@router.put("/{invoice_id}", response_model=schemas.InvoiceResponse)
def update_invoice(
    invoice_id: int,
    invoice: schemas.InvoiceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("factura.editar"))
):
    service = InvoiceService(db)
    return service.update_invoice(invoice_id, invoice, current_user.id)

@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("factura.eliminar"))
):
    service = InvoiceService(db)
    service.delete_invoice(invoice_id)
    return None
