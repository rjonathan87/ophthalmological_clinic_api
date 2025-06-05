from app.data.repositories.role_repository import RoleRepository
from app.domain.schemas import RoleCreate, RoleUpdate, RoleInDB
from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status

class RoleService:
    def __init__(self, db: Session):
        self.repository = RoleRepository(db)

    def create_role(self, role: RoleCreate) -> RoleInDB:
        if self.repository.get_by_name(role.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role with name '{role.name}' already exists"
            )
        return self.repository.create(role)

    def get_role(self, role_id: int) -> RoleInDB:
        role = self.repository.get_by_id(role_id)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id {role_id} not found"
            )
        return role

    def get_roles(self, skip: int = 0, limit: int = 100) -> List[RoleInDB]:
        return self.repository.get_all(skip, limit)

    def update_role(self, role_id: int, role: RoleUpdate) -> RoleInDB:
        updated_role = self.repository.update(role_id, role)
        if not updated_role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id {role_id} not found"
            )
        return updated_role

    def delete_role(self, role_id: int) -> bool:
        if not self.repository.delete(role_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with id {role_id} not found"
            )
        return True