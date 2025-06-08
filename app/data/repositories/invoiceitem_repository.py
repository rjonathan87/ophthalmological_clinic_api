from sqlalchemy.orm import Session
from app.domain.models.invoiceitem import InvoiceItem
from app.domain.schemas import InvoiceItemCreate, InvoiceItemUpdate
from typing import List, Optional
from fastapi import HTTPException, status

class InvoiceItemRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, invoice_item: InvoiceItemCreate) -> InvoiceItem:
        db_item = InvoiceItem(**invoice_item.model_dump())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def get_by_id(self, item_id: int) -> Optional[InvoiceItem]:
        return self.db.query(InvoiceItem).filter(InvoiceItem.id == item_id).first()

    def get_by_invoice_id(self, invoice_id: int) -> List[InvoiceItem]:
        return self.db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[InvoiceItem]:
        return self.db.query(InvoiceItem).offset(skip).limit(limit).all()

    def update(self, item_id: int, item: InvoiceItemUpdate) -> Optional[InvoiceItem]:
        db_item = self.get_by_id(item_id)
        if db_item:
            for key, value in item.model_dump(exclude_unset=True).items():
                setattr(db_item, key, value)
            self.db.commit()
            self.db.refresh(db_item)
            return db_item
        return None

    def delete(self, item_id: int) -> bool:
        db_item = self.get_by_id(item_id)
        if db_item:
            self.db.delete(db_item)
            self.db.commit()
            return True
        return False
