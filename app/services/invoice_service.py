from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.data.repositories.invoice_repository import InvoiceRepository
from app.domain import schemas
from typing import List, Optional

class InvoiceService:
    def __init__(self, db: Session):
        self.repository = InvoiceRepository(db)
    
    def create_invoice(self, invoice: schemas.InvoiceCreate, created_by_user_id: int) -> schemas.InvoiceInDB:
        # Validar monto total
        if invoice.total != round(invoice.subtotal + invoice.tax, 2):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Total amount must equal subtotal plus tax"
            )
        
        return self.repository.create(invoice, created_by_user_id)
    
    def get_invoice(self, invoice_id: int) -> schemas.InvoiceInDB:
        invoice = self.repository.get_by_id(invoice_id)
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice not found"
            )
        return invoice
    
    def get_invoices(self, skip: int = 0, limit: int = 100) -> List[schemas.InvoiceInDB]:
        return self.repository.get_all(skip, limit)
    
    def get_patient_invoices(self, patient_id: int, skip: int = 0, limit: int = 100) -> List[schemas.InvoiceInDB]:
        return self.repository.get_by_patient_id(patient_id, skip, limit)
    
    def get_clinic_invoices(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[schemas.InvoiceInDB]:
        return self.repository.get_by_clinic_id(clinic_id, skip, limit)
    
    def get_consultation_invoices(self, consultation_id: int, skip: int = 0, limit: int = 100) -> List[schemas.InvoiceInDB]:
        return self.repository.get_by_consultation_id(consultation_id, skip, limit)
    
    def get_appointment_invoices(self, appointment_id: int, skip: int = 0, limit: int = 100) -> List[schemas.InvoiceInDB]:
        return self.repository.get_by_appointment_id(appointment_id, skip, limit)
    
    def update_invoice(self, invoice_id: int, invoice: schemas.InvoiceUpdate, updated_by_user_id: int) -> schemas.InvoiceInDB:
        updated_invoice = self.repository.update(invoice_id, invoice, updated_by_user_id)
        if not updated_invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice not found"
            )
        return updated_invoice
    
    def delete_invoice(self, invoice_id: int) -> bool:
        if not self.repository.delete(invoice_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice not found"
            )
        return True
    
    def search_invoices(self, search_term: str, clinic_id: Optional[int] = None) -> List[schemas.InvoiceInDB]:
        return self.repository.search_invoices(search_term, clinic_id)
