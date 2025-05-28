from sqlalchemy.orm import Session
from app.domain import schemas, models
from app.data.repositories.user_repository import UserRepository, get_password_hash
from app.data.repositories.role_repository import RoleRepository
from fastapi import HTTPException, status

class UserService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
        self.role_repo = RoleRepository(db) # Para validar que el rol existe

    def get_user(self, user_id: int):
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def get_user_by_username(self, username: str):
        user = self.user_repo.get_user_by_username(username)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def create_user(self, user_create: schemas.UserCreate):
        if self.user_repo.get_user_by_username(user_create.username):
            raise HTTPException(status_code=400, detail="Username already registered")
        if self.user_repo.get_user_by_email(user_create.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        if user_create.role_id:
            role = self.role_repo.get_role_by_id(user_create.role_id)
            if not role:
                raise HTTPException(status_code=400, detail="Role not found")

        return self.user_repo.create_user(user_create)

    def get_all_users(self, skip: int = 0, limit: int = 100):
        return self.user_repo.get_users(skip=skip, limit=limit)

    def update_user(self, user_id: int, user_update: schemas.UserUpdate):
        existing_user = self.user_repo.get_user_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        if user_update.email and user_update.email != existing_user.email:
            if self.user_repo.get_user_by_email(user_update.email):
                raise HTTPException(status_code=400, detail="Email already registered by another user")

        if user_update.role_id:
            role = self.role_repo.get_role_by_id(user_update.role_id)
            if not role:
                raise HTTPException(status_code=400, detail="Role not found")

        return self.user_repo.update_user(user_id, user_update)

    def delete_user(self, user_id: int):
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        self.user_repo.delete_user(user_id)
        return {"message": "User deleted successfully"}