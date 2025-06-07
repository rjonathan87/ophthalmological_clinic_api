from typing import List
from sqlalchemy.orm import Session
from app.data.repositories.role_permission_repository import RolePermissionRepository
from app.domain.schemas import RolePermissionCreate, RolePermissionInDB
from fastapi import HTTPException

class RolePermissionService:
    def __init__(self, db: Session):
        self.repository = RolePermissionRepository(db)

    def assign_permission(self, role_permission: RolePermissionCreate) -> RolePermissionInDB:
        # Verificar si la relación ya existe
        existing = self.repository.get_by_ids(
            role_permission.role_id, 
            role_permission.permission_id
        )
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Esta relación rol-permiso ya existe"
            )
        return self.repository.create(role_permission)

    def get_role_permissions(self, role_id: int) -> List[RolePermissionInDB]:
        return self.repository.get_by_role_id(role_id)

    def get_permission_roles(self, permission_id: int) -> List[RolePermissionInDB]:
        return self.repository.get_by_permission_id(permission_id)

    def remove_permission(self, role_id: int, permission_id: int) -> bool:
        return self.repository.delete(role_id, permission_id)