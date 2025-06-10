from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.domain import schemas
from app.services.lead_service import LeadService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.LeadResponse, status_code=status.HTTP_201_CREATED)
def create_lead(
    lead: schemas.LeadCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("leads.create"))
):
    """
    Crea un nuevo lead en el sistema.
    Requiere el permiso 'leads.create'.
    """
    service = LeadService(db)
    
    # Verificar si ya existe un lead con el mismo teléfono
    existing_lead = service.get_lead_by_mobile_phone(lead.mobile_phone)
    if existing_lead:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un lead con el teléfono {lead.mobile_phone}"
        )
      # Verificar si ya existe un lead con el mismo email (si se proporciona)
    if lead.email:
        existing_email = service.get_lead_by_email(lead.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un lead con el email {lead.email}"
            )
    
    # Verificar si el service_id es válido cuando se proporciona
    if lead.service_id is not None:
        from app.services.service_service import ServiceService
        service_service = ServiceService(db)
        try:
            service_service.get_service(lead.service_id)
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El servicio con ID {lead.service_id} no existe"
            )
    
    return service.create_lead(lead)

@router.get("/", response_model=List[schemas.LeadResponse])
def get_leads(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = Query(None, description="Filtrar por estado del lead"),
    service_id: Optional[int] = Query(None, description="Filtrar por ID de servicio"),
    channel: Optional[str] = Query(None, description="Filtrar por canal"),
    search: Optional[str] = Query(None, description="Buscar por nombre, apellido, email o teléfono"),
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("leads.read"))
):
    """
    Obtiene una lista de leads con opciones de filtrado.
    Requiere el permiso 'leads.read'.
    """
    service = LeadService(db)
    
    if search:
        return service.search_leads(search, skip, limit)
    elif status:
        return service.get_leads_by_status(status, skip, limit)
    elif service_id:
        return service.get_leads_by_service(service_id, skip, limit)
    elif channel:
        return service.get_leads_by_channel(channel, skip, limit)
    else:
        return service.get_leads(skip, limit)

@router.get("/{lead_id}", response_model=schemas.LeadResponse)
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("leads.read"))
):
    """
    Obtiene un lead por su ID.
    Requiere el permiso 'leads.read'.
    """
    service = LeadService(db)
    db_lead = service.get_lead(lead_id)
    if not db_lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead no encontrado")
    return db_lead

@router.patch("/{lead_id}/status", response_model=schemas.LeadResponse)
def update_lead_status(
    lead_id: int,
    status_update: schemas.LeadStatusUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("leads.update"))
):
    """
    Actualiza solo el estado de un lead.
    Útil cuando el bot pasa de 'new' a 'scheduled'.
    Requiere el permiso 'leads.update'.
    """
    service = LeadService(db)
    db_lead = service.update_lead_status(lead_id, status_update)
    if not db_lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead no encontrado")
    return db_lead

@router.put("/{lead_id}", response_model=schemas.LeadResponse)
def update_lead(
    lead_id: int,
    lead: schemas.LeadUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("leads.update"))
):
    """
    Actualiza un lead existente por su ID.
    Requiere el permiso 'leads.update'.
    """
    service = LeadService(db)
    
    # Verificar si el lead existe
    existing_lead = service.get_lead(lead_id)
    if not existing_lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead no encontrado")
    
    # Verificar si se está actualizando el teléfono y si ya existe otro lead con ese teléfono
    if lead.mobile_phone and lead.mobile_phone != existing_lead.mobile_phone:
        mobile_lead = service.get_lead_by_mobile_phone(lead.mobile_phone)
        if mobile_lead and mobile_lead.lead_id != lead_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe otro lead con el teléfono {lead.mobile_phone}"
            )
      # Verificar si se está actualizando el email y si ya existe otro lead con ese email
    if lead.email and lead.email != existing_lead.email:
        email_lead = service.get_lead_by_email(lead.email)
        if email_lead and email_lead.lead_id != lead_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe otro lead con el email {lead.email}"
            )
    
    # Verificar si el service_id es válido cuando se proporciona
    if lead.service_id is not None and lead.service_id != 0:
        from app.services.service_service import ServiceService
        service_service = ServiceService(db)
        try:
            service_service.get_service(lead.service_id)
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El servicio con ID {lead.service_id} no existe"
            )
    elif lead.service_id == 0:
        # Si se envía service_id=0, lo cambiamos a None para evitar problemas de FK
        lead_dict = lead.dict(exclude_unset=True)
        lead_dict["service_id"] = None
        lead = schemas.LeadUpdate(**lead_dict)
    
    # Verificar si el appointment_id es válido cuando se proporciona
    if lead.appointment_id is not None:
        from app.services.appointment_service import AppointmentService
        appointment_service = AppointmentService(db)
        try:
            appointment_service.get_appointment(lead.appointment_id)
        except HTTPException:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"La cita con ID {lead.appointment_id} no existe"
            )
    
    db_lead = service.update_lead(lead_id, lead)
    return db_lead

@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("leads.delete"))
):
    """
    Elimina un lead por su ID.
    Requiere el permiso 'leads.delete'.
    """
    service = LeadService(db)
    
    # Verificar si el lead existe
    existing_lead = service.get_lead(lead_id)
    if not existing_lead:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lead no encontrado")
    
    success = service.delete_lead(lead_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar el lead")
