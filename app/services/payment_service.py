from fastapi import HTTPException, status
from app.data.repositories.payment_repository import PaymentRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List, Optional

class PaymentService:
    def __init__(self, db: Session):
        self.repository = PaymentRepository(db)

    def create_payment(self, payment: schemas.PaymentCreate, created_by_user_id: int) -> schemas.PaymentInDB:
        return self.repository.create(payment, created_by_user_id)

    def get_payment(self, payment_id: int) -> schemas.PaymentInDB:
        payment = self.repository.get_by_id(payment_id)
        if not payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pago no encontrado"
            )
        return payment

    def get_payments(self, skip: int = 0, limit: int = 100) -> List[schemas.PaymentInDB]:
        return self.repository.get_all(skip, limit)

    def get_invoice_payments(self, invoice_id: int, skip: int = 0, limit: int = 100) -> List[schemas.PaymentInDB]:
        return self.repository.get_by_invoice_id(invoice_id, skip, limit)

    def get_patient_payments(self, patient_id: int, skip: int = 0, limit: int = 100) -> List[schemas.PaymentInDB]:
        return self.repository.get_by_patient_id(patient_id, skip, limit)
    
    def get_clinic_payments(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[schemas.PaymentInDB]:
        return self.repository.get_by_clinic_id(clinic_id, skip, limit)

    def update_payment(self, payment_id: int, payment: schemas.PaymentUpdate, updated_by_user_id: int) -> schemas.PaymentInDB:
        updated_payment = self.repository.update(payment_id, payment, updated_by_user_id)
        if not updated_payment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pago no encontrado"
            )
        return updated_payment

    def delete_payment(self, payment_id: int) -> bool:
        return self.repository.delete(payment_id)
