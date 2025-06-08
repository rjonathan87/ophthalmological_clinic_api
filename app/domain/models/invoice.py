from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.dialects.mysql import JSON

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    clinic_id = Column(Integer, ForeignKey("clinics.id"), nullable=False)
    consultation_id = Column(Integer, ForeignKey("consultations.id"), nullable=True)
    appointment_id = Column(Integer, ForeignKey("appointments.id"), nullable=True)
    
    invoice_number = Column(String(50), unique=True, nullable=False)
    issue_date = Column(DateTime, nullable=False, default=func.now())
    due_date = Column(DateTime, nullable=False)
    subtotal = Column(Float, nullable=False)
    tax = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    payment_status = Column(String(50), nullable=False, default='Pending') # Pending, Paid, Partially Paid, Overdue, Cancelled, Refunded
    payment_method = Column(String(50)) # Cash, Credit Card, Bank Transfer, Insurance, etc.
    notes = Column(Text)
    
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    created_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    updated_by_user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    deleted_at = Column(DateTime)

    # Relationships
    patient = relationship("Patient", back_populates="invoices")
    clinic = relationship("Clinic", back_populates="invoices")
    consultation = relationship("Consultation", back_populates="invoices")
    appointment = relationship("Appointment", back_populates="invoices")    
    created_by_user = relationship("User", foreign_keys=[created_by_user_id], back_populates="created_invoices")
    updated_by_user = relationship("User", foreign_keys=[updated_by_user_id], back_populates="updated_invoices")
    invoice_items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="invoice")
