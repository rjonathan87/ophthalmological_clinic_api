from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.invoiceitem_service import InvoiceItemService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.InvoiceItemResponse, status_code=status.HTTP_201_CREATED)
def create_invoice_item(
    invoice_item: schemas.InvoiceItemCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("billing.create_invoice"))
):
    """
    Crear un nuevo ítem de factura.
    Requiere el permiso: billing.create_invoice
    """
    service = InvoiceItemService(db)
    return service.create_invoice_item(invoice_item)

@router.get("/", response_model=List[schemas.InvoiceItemResponse])
def get_invoice_items(
    skip: int = 0,
    limit: int = 100,
    invoice_id: Optional[int] = Query(None),
    service_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("billing.read_invoice"))
):
    """
    Obtener lista de ítems de factura.
    Requiere el permiso: billing.read_invoice
    """
    service = InvoiceItemService(db)
    return service.get_invoice_items(
        skip=skip,
        limit=limit,
        invoice_id=invoice_id,
        service_id=service_id
    )

@router.get("/{invoice_item_id}", response_model=schemas.InvoiceItemResponse)
def get_invoice_item(
    invoice_item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("billing.read_invoice"))
):
    """
    Obtener un ítem de factura específico por ID.
    Requiere el permiso: billing.read_invoice
    """
    service = InvoiceItemService(db)
    return service.get_invoice_item(invoice_item_id)

@router.put("/{invoice_item_id}", response_model=schemas.InvoiceItemResponse)
def update_invoice_item(
    invoice_item_id: int,
    invoice_item: schemas.InvoiceItemUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("billing.update_invoice"))
):
    """
    Actualizar un ítem de factura.
    Requiere el permiso: billing.update_invoice
    """
    service = InvoiceItemService(db)
    return service.update_invoice_item(invoice_item_id, invoice_item)

@router.delete("/{invoice_item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice_item(
    invoice_item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("billing.delete_invoice"))
):
    """
    Eliminar un ítem de factura.
    Requiere el permiso: billing.delete_invoice
    """
    service = InvoiceItemService(db)
    service.delete_invoice_item(invoice_item_id)
    return {"message": "Invoice item deleted successfully"}
