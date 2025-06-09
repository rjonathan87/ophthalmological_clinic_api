from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.invoice_service import InvoiceService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.InvoiceResponse)
def create_invoice(
    invoice: schemas.InvoiceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("billing.create_invoice"))
):
    service = InvoiceService(db)
    return service.create_invoice(invoice)

@router.get("/", response_model=List[schemas.InvoiceResponse])
def get_invoices(
    skip: int = 0,
    limit: int = 100,
    clinic_id: Optional[int] = Query(None),
    patient_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("billing.read_invoice"))
):
    service = InvoiceService(db)
    return service.get_invoices(
        skip=skip,
        limit=limit,
        clinic_id=clinic_id,
        patient_id=patient_id,
        status=status
    )

@router.get("/{invoice_id}", response_model=schemas.InvoiceResponse)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("billing.read_invoice"))
):
    service = InvoiceService(db)
    return service.get_invoice(invoice_id)

@router.put("/{invoice_id}", response_model=schemas.InvoiceResponse)
def update_invoice(
    invoice_id: int,
    invoice: schemas.InvoiceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("billing.update_invoice"))
):
    service = InvoiceService(db)
    return service.update_invoice(invoice_id, invoice)

@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("billing.delete_invoice"))
):
    service = InvoiceService(db)
    service.delete_invoice(invoice_id)
    return {"message": "Invoice deleted successfully"}
