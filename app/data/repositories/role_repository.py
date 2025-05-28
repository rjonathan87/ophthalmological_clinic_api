from sqlalchemy.orm import Session
from app.domain import models
from app.domain import schemas

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_role_by_id(self, role_id: int):
        return self.db.query(models.Role).filter(models.Role.id == role_id).first()

    def get_role_by_name(self, name: str):
        return self.db.query(models.Role).filter(models.Role.name == name).first()

    def get_roles(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.Role).offset(skip).limit(limit).all()

    def create_role(self, role: schemas.RoleCreate):
        db_role = models.Role(name=role.name, description=role.description)
        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role

    def update_role(self, role_id: int, role_update: schemas.RoleUpdate):
        db_role = self.get_role_by_id(role_id)
        if db_role:
            update_data = role_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_role, key, value)
            self.db.add(db_role)
            self.db.commit()
            self.db.refresh(db_role)
        return db_role

    def delete_role(self, role_id: int):
        db_role = self.get_role_by_id(role_id)
        if db_role:
            self.db.delete(db_role)
            self.db.commit()
        return db_role