from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.domain import schemas
from app.services.user_service import UserService
from app.api.dependencies import get_current_user, require_permission
from app.domain.models import User as DBUser # Alias para evitar conflicto de nombres

users_router = APIRouter()

@users_router.post("/", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("users.create"))
):
    user_service = UserService(db)
    return user_service.create_user(user)

@users_router.get("/", response_model=List[schemas.UserResponse])
def get_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("users.read"))
):
    user_service = UserService(db)
    return user_service.get_all_users(current_user=current_user, skip=skip, limit=limit)

@users_router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("users.read"))
):
    user_service = UserService(db)
    return user_service.get_user(user_id)

@users_router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(
    user_id: int,
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    user_service = UserService(db)
    # Permite al usuario actualizar su propio perfil o a alguien con permisos actualizar cualquier perfil
    if current_user.id == user_id or (current_user.role and any(
        perm.name == "users.manage" 
        for perm in current_user.role.permissions
    )):
        return user_service.update_user(user_id, user_update)
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(require_permission("users.manage"))
):
    user_service = UserService(db)
    user_service.delete_user(user_id)
    return {"message": "User deleted successfully"}
