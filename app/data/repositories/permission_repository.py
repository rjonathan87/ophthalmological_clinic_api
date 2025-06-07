from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from app.domain.models.permission import Permission
from app.domain.schemas import PermissionCreate, PermissionUpdate
from typing import List, Optional

class PermissionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, permission: PermissionCreate) -> Permission:
        try:
            db_permission = Permission(**permission.dict())
            self.db.add(db_permission)
            self.db.commit()
            self.db.refresh(db_permission)
            return db_permission
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El permiso con ese nombre ya existe"
            )

    def get_by_id(self, permission_id: int) -> Optional[Permission]:
        return self.db.query(Permission).filter(Permission.id == permission_id).first()

    def get_by_name(self, name: str) -> Optional[Permission]:
        return self.db.query(Permission).filter(Permission.name == name).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Permission]:
        return self.db.query(Permission).offset(skip).limit(limit).all()

    def update(self, permission_id: int, permission: PermissionUpdate) -> Optional[Permission]:
        try:
            db_permission = self.get_by_id(permission_id)
            if db_permission:
                for key, value in permission.dict(exclude_unset=True).items():
                    setattr(db_permission, key, value)
                self.db.commit()
                self.db.refresh(db_permission)
                return db_permission
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre del permiso ya existe"
            )
        return None

    def delete(self, permission_id: int) -> bool:
        db_permission = self.get_by_id(permission_id)
        if db_permission:
            self.db.delete(db_permission)
            self.db.commit()
            return True
        return False