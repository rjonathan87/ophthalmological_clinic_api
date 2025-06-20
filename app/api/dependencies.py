from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import get_current_user_from_token
from app.domain.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user = get_current_user_from_token(db, token)
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")
    return user

def has_role(required_role_name: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if not current_user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario sin rol asignado"
            )
            
        # El superadmin tiene acceso a todo
        if current_user.role.name == 'superadmin':
            return current_user
            
        if current_user.role.name != required_role_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permisos insuficientes"
            )
        return current_user
    return role_checker

def require_permission(permission_name: str):
    async def _require_permission(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        if not current_user.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario sin rol asignado"
            )
        
        # El superadmin tiene todos los permisos
        if current_user.role.name == 'superadmin':
            return current_user
            
        # Verificar si el rol tiene el permiso requerido
        has_permission = any(
            perm.name == permission_name 
            for perm in current_user.role.permissions
        )
        
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permisos insuficientes"
            )
        return current_user
    return _require_permission

# Decoradores específicos para roles comunes
def is_admin(current_user: User = Depends(get_current_user)):
    return has_role("admin")(current_user)

def is_doctor(current_user: User = Depends(get_current_user)):
    return has_role("doctor")(current_user)

def is_receptionist(current_user: User = Depends(get_current_user)):
    return has_role("receptionist")(current_user)

def is_assistant(current_user: User = Depends(get_current_user)):
    return has_role("assistant")(current_user)

def is_patient(current_user: User = Depends(get_current_user)):
    return has_role("patient")(current_user)
