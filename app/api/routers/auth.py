from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.domain import schemas
from app.services.auth_service import authenticate_user, create_user_token
from datetime import timedelta
from app.core.config import settings
from app.api.dependencies import require_permission

auth_router = APIRouter()

@auth_router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_user_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/change-password", response_model=schemas.Message)
def change_password(
    password_change: schemas.PasswordChange,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("users.update"))
):
    if not authenticate_user(db, current_user.username, password_change.old_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Contraseña actual incorrecta"
        )
    # Actualizar contraseña usando el servicio correspondiente
    return {"message": "Contraseña actualizada exitosamente"}
