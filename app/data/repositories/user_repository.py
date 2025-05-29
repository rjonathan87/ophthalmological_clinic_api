from sqlalchemy.orm import Session, joinedload
from app.domain import models
from app.domain import schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int):
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def get_user_by_username(self, username: str):
        return self.db.query(models.User).filter(models.User.username == username).first()

    def get_user_by_email(self, email: str):
        return self.db.query(models.User).filter(models.User.email == email).first()

    def create_user(self, user: schemas.UserCreate):
        hashed_password = get_password_hash(user.password)
        db_user = models.User(
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            hashed_password=hashed_password,
            full_name=user.full_name,
            role_id=user.role_id,
            associated_clinic_id=user.associated_clinic_id,
            is_active=True # Por defecto activo al crear
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_users(self, skip: int = 0, limit: int = 100):
        return self.db.query(models.User)\
            .options(
                joinedload(models.User.role),
                joinedload(models.User.clinic)
            )\
            .offset(skip)\
            .limit(limit)\
            .all()

    def get_users_by_clinic(self, clinic_id: int, skip: int = 0, limit: int = 100):
        return self.db.query(models.User)\
            .filter(models.User.associated_clinic_id == clinic_id)\
            .options(
                joinedload(models.User.role),
                joinedload(models.User.clinic)
            )\
            .offset(skip)\
            .limit(limit)\
            .all()

    def update_user(self, user_id: int, user_update: schemas.UserUpdate):
        db_user = self.get_user_by_id(user_id)
        if db_user:
            update_data = user_update.model_dump(exclude_unset=True)
            if "password" in update_data:
                update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
            for key, value in update_data.items():
                setattr(db_user, key, value)
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        db_user = self.get_user_by_id(user_id)
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
        return db_user
