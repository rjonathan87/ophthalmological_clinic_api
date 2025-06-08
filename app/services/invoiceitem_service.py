from app.data.repositories.invoiceitem_repository import InvoiceItemRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status

class InvoiceItemService:
    def __init__(self, db: Session):
        self.repository = InvoiceItemRepository(db)

    def create_invoice_item(self, invoice_item: schemas.InvoiceItemCreate) -> schemas.InvoiceItemInDB:
        # TODO: Validar que la factura y el servicio existan
        return self.repository.create(invoice_item)

    def get_invoice_item(self, item_id: int) -> schemas.InvoiceItemInDB:
        db_item = self.repository.get_by_id(item_id)
        if db_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item de factura no encontrado"
            )
        return db_item

    def get_invoice_items_by_invoice(self, invoice_id: int) -> List[schemas.InvoiceItemInDB]:
        return self.repository.get_by_invoice_id(invoice_id)

    def get_invoice_items(self, skip: int = 0, limit: int = 100) -> List[schemas.InvoiceItemInDB]:
        return self.repository.get_all(skip, limit)

    def update_invoice_item(self, item_id: int, item: schemas.InvoiceItemUpdate) -> schemas.InvoiceItemInDB:
        updated_item = self.repository.update(item_id, item)
        if updated_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item de factura no encontrado"
            )
        return updated_item

    def delete_invoice_item(self, item_id: int) -> bool:
        if not self.repository.delete(item_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Item de factura no encontrado"
            )
        return True
