from app.data.repositories.permission_repository import PermissionRepository
from app.domain.schemas import PermissionCreate, PermissionUpdate, PermissionInDB
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status

class PermissionService:
    def __init__(self, db: Session):
        self.repository = PermissionRepository(db)

    def create_permission(self, permission: PermissionCreate) -> PermissionInDB:
        return self.repository.create(permission)

    def get_permission(self, permission_id: int) -> Optional[PermissionInDB]:
        permission = self.repository.get_by_id(permission_id)
        if not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permiso no encontrado"
            )
        return permission

    def get_permissions(self, skip: int = 0, limit: int = 100) -> List[PermissionInDB]:
        return self.repository.get_all(skip, limit)

    def update_permission(self, permission_id: int, permission: PermissionUpdate) -> PermissionInDB:
        updated_permission = self.repository.update(permission_id, permission)
        if not updated_permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permiso no encontrado"
            )
        return updated_permission

    def delete_permission(self, permission_id: int) -> bool:
        if not self.repository.delete(permission_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Permiso no encontrado"
            )
        return True