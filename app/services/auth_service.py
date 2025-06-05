from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from app.core.config import settings
from app.domain import schemas
from app.data.repositories.user_repository import UserRepository, verify_password
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.domain.models import Role, RolePermission

ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_user_token(user):
    return create_access_token(
        data={
            "sub": user.username,
            "role_id": user.role_id,
            "clinic_id": user.associated_clinic_id
        }
    )

def authenticate_user(db: Session, username: str, password: str):
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_username(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def get_current_user_from_token(db: Session, token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    user_repo = UserRepository(db)
    user = user_repo.get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    
    # Cargar relaciones necesarias
    user = db.query(user.__class__)\
        .filter(user.__class__.id == user.id)\
        .options(
            joinedload(user.__class__.role)
            .subqueryload(Role.role_permissions)
            .joinedload(RolePermission.permission)
        )\
        .first()
    
    return user
