from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.domain.schemas import RoleCreate, RoleUpdate, RoleInDB
from app.services.role_service import RoleService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter(
    # prefix="/roles",
    tags=["Roles"]
)

@router.post("/", response_model=RoleInDB, status_code=status.HTTP_201_CREATED)
def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("roles.create"))
):
    service = RoleService(db)
    return service.create_role(role)

@router.get("/", response_model=List[RoleInDB])
def get_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("roles.read"))
):
    service = RoleService(db)
    return service.get_roles(skip, limit)

@router.get("/{role_id}", response_model=RoleInDB)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("roles.read"))
):
    service = RoleService(db)
    return service.get_role(role_id)

@router.put("/{role_id}", response_model=RoleInDB)
def update_role(
    role_id: int,
    role: RoleUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("roles.update"))
):
    service = RoleService(db)
    return service.update_role(role_id, role)

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("roles.delete"))
):
    service = RoleService(db)
    service.delete_role(role_id)