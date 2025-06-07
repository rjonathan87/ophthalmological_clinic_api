from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.domain.schemas import RolePermissionCreate, RolePermissionInDB
from app.services.role_permission_service import RolePermissionService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=RolePermissionInDB)
def assign_permission(
    role_permission: RolePermissionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.gestionar_roles"))
):
    service = RolePermissionService(db)
    return service.assign_permission(role_permission)

@router.get("/role/{role_id}", response_model=List[RolePermissionInDB])
def get_role_permissions(
    role_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.gestionar_roles"))
):
    service = RolePermissionService(db)
    return service.get_role_permissions(role_id)

@router.delete("/{role_id}/{permission_id}")
def remove_permission(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("admin.gestionar_roles"))
):
    service = RolePermissionService(db)
    if not service.remove_permission(role_id, permission_id):
        raise HTTPException(
            status_code=404,
            detail="Relación rol-permiso no encontrada"
        )
    return {"message": "Permiso removido exitosamente"}