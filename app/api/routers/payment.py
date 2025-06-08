from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.payment_service import PaymentService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.PaymentResponse)
def create_payment(
    payment: schemas.PaymentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("pago.crear"))
):
    service = PaymentService(db)
    return service.create_payment(payment, current_user.id)

@router.get("/", response_model=List[schemas.PaymentResponse])
def get_payments(
    invoice_id: Optional[int] = None,
    patient_id: Optional[int] = None,
    clinic_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("pago.ver"))
):
    service = PaymentService(db)
    
    if invoice_id:
        return service.get_invoice_payments(invoice_id, skip, limit)
    elif patient_id:
        return service.get_patient_payments(patient_id, skip, limit)
    elif clinic_id:
        return service.get_clinic_payments(clinic_id, skip, limit)
    return service.get_payments(skip, limit)

@router.get("/{payment_id}", response_model=schemas.PaymentResponse)
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("pago.ver"))
):
    service = PaymentService(db)
    return service.get_payment(payment_id)

@router.put("/{payment_id}", response_model=schemas.PaymentResponse)
def update_payment(
    payment_id: int,
    payment: schemas.PaymentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("pago.actualizar"))
):
    service = PaymentService(db)
    return service.update_payment(payment_id, payment, current_user.id)

@router.delete("/{payment_id}")
def delete_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("pago.eliminar"))
):
    service = PaymentService(db)
    if not service.delete_payment(payment_id):
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return {"message": "Pago eliminado exitosamente"}
