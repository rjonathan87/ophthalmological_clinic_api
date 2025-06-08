from sqlalchemy.orm import Session
from app.domain import schemas
from app.domain.models import Payment
from typing import List, Optional
from sqlalchemy import or_, func

class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, payment: schemas.PaymentCreate, created_by_user_id: int) -> Payment:
        db_payment = Payment(
            **payment.model_dump(),
            created_by_user_id=created_by_user_id
        )
        self.db.add(db_payment)
        self.db.commit()
        self.db.refresh(db_payment)
        return db_payment
    
    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        return self.db.query(Payment).filter(
            Payment.id == payment_id,
            Payment.deleted_at == None
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Payment]:
        return self.db.query(Payment).filter(
            Payment.deleted_at == None
        ).offset(skip).limit(limit).all()
    
    def get_by_invoice_id(self, invoice_id: int, skip: int = 0, limit: int = 100) -> List[Payment]:
        return self.db.query(Payment).filter(
            Payment.invoice_id == invoice_id,
            Payment.deleted_at == None
        ).offset(skip).limit(limit).all()
    
    def get_by_patient_id(self, patient_id: int, skip: int = 0, limit: int = 100) -> List[Payment]:
        return self.db.query(Payment).filter(
            Payment.patient_id == patient_id,
            Payment.deleted_at == None
        ).offset(skip).limit(limit).all()
    
    def get_by_clinic_id(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[Payment]:
        return self.db.query(Payment).filter(
            Payment.clinic_id == clinic_id,
            Payment.deleted_at == None
        ).offset(skip).limit(limit).all()

    def update(self, payment_id: int, payment: schemas.PaymentUpdate, updated_by_user_id: int) -> Optional[Payment]:
        db_payment = self.get_by_id(payment_id)
        if db_payment:
            payment_data = payment.model_dump(exclude_unset=True)
            payment_data["updated_by_user_id"] = updated_by_user_id
            for key, value in payment_data.items():
                setattr(db_payment, key, value)
            self.db.commit()
            self.db.refresh(db_payment)
        return db_payment

    def delete(self, payment_id: int) -> bool:
        payment = self.get_by_id(payment_id)
        if payment:
            payment.deleted_at = func.now()
            self.db.commit()
            return True
        return False
