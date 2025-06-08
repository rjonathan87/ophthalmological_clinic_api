from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.dialects.mysql import JSON

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False, default=func.now())
    payment_method = Column(String(50), nullable=False) # Cash, Credit Card, Bank Transfer, Insurance, etc.
    transaction_id = Column(String(100))  # For electronic payments
    payment_status = Column(String(50), nullable=False, default='Processed') # Processed, Failed, Refunded, Voided
    notes = Column(Text)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    deleted_at = Column(DateTime)

    # Relationships
    invoice = relationship("Invoice", back_populates="payments")
    patient = relationship("Patient", back_populates="payments")
    clinic = relationship("Clinic", back_populates="payments")
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_payments")
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_payments")
