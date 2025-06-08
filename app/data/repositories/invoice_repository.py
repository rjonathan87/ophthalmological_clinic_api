from sqlalchemy.orm import Session
from app.domain import schemas
from app.domain.models import Invoice
from typing import List, Optional
from sqlalchemy import or_

class InvoiceRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, invoice: schemas.InvoiceCreate, created_by_user_id: int) -> Invoice:
        db_invoice = Invoice(**invoice.model_dump(), created_by_user_id=created_by_user_id)
        self.db.add(db_invoice)
        self.db.commit()
        self.db.refresh(db_invoice)
        return db_invoice

    def get_by_id(self, invoice_id: int) -> Optional[Invoice]:
        return self.db.query(Invoice).filter(
            Invoice.id == invoice_id,
            Invoice.deleted_at == None
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Invoice]:
        return self.db.query(Invoice).filter(
            Invoice.deleted_at == None
        ).offset(skip).limit(limit).all()

    def get_by_patient_id(self, patient_id: int, skip: int = 0, limit: int = 100) -> List[Invoice]:
        return self.db.query(Invoice).filter(
            Invoice.patient_id == patient_id,
            Invoice.deleted_at == None
        ).offset(skip).limit(limit).all()
    
    def get_by_clinic_id(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[Invoice]:
        return self.db.query(Invoice).filter(
            Invoice.clinic_id == clinic_id,
            Invoice.deleted_at == None
        ).offset(skip).limit(limit).all()

    def get_by_consultation_id(self, consultation_id: int, skip: int = 0, limit: int = 100) -> List[Invoice]:
        return self.db.query(Invoice).filter(
            Invoice.consultation_id == consultation_id,
            Invoice.deleted_at == None
        ).offset(skip).limit(limit).all()

    def get_by_appointment_id(self, appointment_id: int, skip: int = 0, limit: int = 100) -> List[Invoice]:
        return self.db.query(Invoice).filter(
            Invoice.appointment_id == appointment_id,
            Invoice.deleted_at == None
        ).offset(skip).limit(limit).all()

    def update(self, invoice_id: int, invoice: schemas.InvoiceUpdate, updated_by_user_id: int) -> Optional[Invoice]:
        db_invoice = self.get_by_id(invoice_id)
        if db_invoice:
            update_data = invoice.model_dump(exclude_unset=True)
            update_data['updated_by_user_id'] = updated_by_user_id
            for field, value in update_data.items():
                setattr(db_invoice, field, value)
            self.db.commit()
            self.db.refresh(db_invoice)
        return db_invoice

    def delete(self, invoice_id: int) -> bool:
        db_invoice = self.get_by_id(invoice_id)
        if db_invoice:
            db_invoice.deleted_at = func.now()
            self.db.commit()
            return True
        return False

    def search_invoices(self, search_term: str, clinic_id: Optional[int] = None) -> List[Invoice]:
        query = self.db.query(Invoice).filter(Invoice.deleted_at == None)
        
        if clinic_id:
            query = query.filter(Invoice.clinic_id == clinic_id)
            
        return query.filter(
            or_(
                Invoice.invoice_number.ilike(f"%{search_term}%"),
                Invoice.payment_status.ilike(f"%{search_term}%"),
                Invoice.payment_method.ilike(f"%{search_term}%"),
                Invoice.notes.ilike(f"%{search_term}%")
            )
        ).all()
