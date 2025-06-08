from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.domain import schemas
from app.services.invoiceitem_service import InvoiceItemService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.InvoiceItemInDB, status_code=status.HTTP_201_CREATED)
def create_invoice_item(
    invoice_item: schemas.InvoiceItemCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("facturas.crear"))
):
    """
    Crear un nuevo ítem de factura.
    Requiere el permiso: facturas.crear
    """
    service = InvoiceItemService(db)
    return service.create_invoice_item(invoice_item)

@router.get("/", response_model=List[schemas.InvoiceItemInDB])
def get_invoice_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("facturas.ver"))
):
    """
    Obtener lista de ítems de factura.
    Requiere el permiso: facturas.ver
    """
    service = InvoiceItemService(db)
    return service.get_invoice_items(skip, limit)

@router.get("/{item_id}", response_model=schemas.InvoiceItemInDB)
def get_invoice_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("facturas.ver"))
):
    """
    Obtener un ítem de factura específico por ID.
    Requiere el permiso: facturas.ver
    """
    service = InvoiceItemService(db)
    return service.get_invoice_item(item_id)

@router.get("/invoice/{invoice_id}", response_model=List[schemas.InvoiceItemInDB])
def get_invoice_items_by_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("facturas.ver"))
):
    """
    Obtener todos los ítems de una factura específica.
    Requiere el permiso: facturas.ver
    """
    service = InvoiceItemService(db)
    return service.get_invoice_items_by_invoice(invoice_id)

@router.put("/{item_id}", response_model=schemas.InvoiceItemInDB)
def update_invoice_item(
    item_id: int,
    invoice_item: schemas.InvoiceItemUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("facturas.editar"))
):
    """
    Actualizar un ítem de factura.
    Requiere el permiso: facturas.editar
    """
    service = InvoiceItemService(db)
    return service.update_invoice_item(item_id, invoice_item)

@router.delete("/{item_id}")
def delete_invoice_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("facturas.eliminar"))
):
    """
    Eliminar un ítem de factura.
    Requiere el permiso: facturas.eliminar
    """
    service = InvoiceItemService(db)
    service.delete_invoice_item(item_id)
    return {"message": "Item de factura eliminado exitosamente"}
