from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.domain.schemas import PermissionCreate, PermissionUpdate, PermissionInDB
from app.services.permission_service import PermissionService
from app.api.dependencies import require_permission

router = APIRouter(
    tags=["Permissions"]
)

@router.post("/", response_model=PermissionInDB, status_code=status.HTTP_201_CREATED)
def create_permission(
    permission: PermissionCreate,
    db: Session = Depends(get_db),
    _=Depends(require_permission("admin.manage_roles"))
):
    service = PermissionService(db)
    return service.create_permission(permission)

@router.get("/", response_model=List[PermissionInDB])
def get_permissions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _=Depends(require_permission("admin.manage_roles"))
):
    service = PermissionService(db)
    return service.get_permissions(skip, limit)

@router.get("/{permission_id}", response_model=PermissionInDB)
def get_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_permission("admin.manage_roles"))
):
    service = PermissionService(db)
    return service.get_permission(permission_id)

@router.put("/{permission_id}", response_model=PermissionInDB)
def update_permission(
    permission_id: int,
    permission: PermissionUpdate,
    db: Session = Depends(get_db),
    _=Depends(require_permission("admin.manage_roles"))
):
    service = PermissionService(db)
    return service.update_permission(permission_id, permission)

@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    _=Depends(require_permission("admin.manage_roles"))
):
    service = PermissionService(db)
    service.delete_permission(permission_id)
    return None