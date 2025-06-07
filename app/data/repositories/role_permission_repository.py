from sqlalchemy.orm import Session
from typing import List, Optional
from app.domain.models.rolepermission import RolePermission
from app.domain.schemas import RolePermissionCreate, RolePermissionUpdate

class RolePermissionRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, role_permission: RolePermissionCreate) -> RolePermission:
        db_role_permission = RolePermission(**role_permission.dict())
        self.db.add(db_role_permission)
        self.db.commit()
        self.db.refresh(db_role_permission)
        return db_role_permission

    def get_by_ids(self, role_id: int, permission_id: int) -> Optional[RolePermission]:
        return self.db.query(RolePermission).filter(
            RolePermission.role_id == role_id,
            RolePermission.permission_id == permission_id
        ).first()

    def get_by_role_id(self, role_id: int) -> List[RolePermission]:
        return self.db.query(RolePermission).filter(RolePermission.role_id == role_id).all()

    def get_by_permission_id(self, permission_id: int) -> List[RolePermission]:
        return self.db.query(RolePermission).filter(RolePermission.permission_id == permission_id).all()

    def delete(self, role_id: int, permission_id: int) -> bool:
        db_role_permission = self.get_by_ids(role_id, permission_id)
        if db_role_permission:
            self.db.delete(db_role_permission)
            self.db.commit()
            return True
        return False