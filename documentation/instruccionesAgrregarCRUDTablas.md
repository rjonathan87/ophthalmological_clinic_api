### Te ayudo a explicar los pasos para agregar nuevos CRUD siguiendo la arquitectura actual del sistema que usa FastAPI con un patrón Repository y Service:

1. **Definir el Modelo en models.py**:
```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class NewTable(Base):
    __tablename__ = "table_name"
    id = Column(Integer, primary_key=True, index=True)
    # ... otros campos
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
```

2. **Crear Schemas en schemas.py**:
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NewTableBase(BaseModel):
    # Campos base
    name: str
    description: Optional[str] = None

class NewTableCreate(NewTableBase):
    # Campos adicionales para creación
    pass

class NewTableUpdate(NewTableBase):
    # Campos que se pueden actualizar
    pass

class NewTableInDB(NewTableBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
```

3. **Crear Repository en `app/data/repositories/new_table_repository.py`**:
```python
from sqlalchemy.orm import Session
from app.domain import models, schemas
from typing import List

class NewTableRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, item: schemas.NewTableCreate) -> models.NewTable:
        db_item = models.NewTable(**item.dict())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def get_by_id(self, item_id: int) -> models.NewTable:
        return self.db.query(models.NewTable).filter(models.NewTable.id == item_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[models.NewTable]:
        return self.db.query(models.NewTable).offset(skip).limit(limit).all()

    def update(self, item_id: int, item: schemas.NewTableUpdate) -> models.NewTable:
        db_item = self.get_by_id(item_id)
        if db_item:
            for key, value in item.dict(exclude_unset=True).items():
                setattr(db_item, key, value)
            self.db.commit()
            self.db.refresh(db_item)
        return db_item

    def delete(self, item_id: int) -> bool:
        db_item = self.get_by_id(item_id)
        if db_item:
            self.db.delete(db_item)
            self.db.commit()
            return True
        return False
```

4. **Crear Service en `app/services/new_table_service.py`**:
```python
from app.data.repositories.new_table_repository import NewTableRepository
from app.domain import schemas
from sqlalchemy.orm import Session
from typing import List

class NewTableService:
    def __init__(self, db: Session):
        self.repository = NewTableRepository(db)

    def create_item(self, item: schemas.NewTableCreate) -> schemas.NewTableInDB:
        return self.repository.create(item)

    def get_item(self, item_id: int) -> schemas.NewTableInDB:
        return self.repository.get_by_id(item_id)

    def get_items(self, skip: int = 0, limit: int = 100) -> List[schemas.NewTableInDB]:
        return self.repository.get_all(skip, limit)

    def update_item(self, item_id: int, item: schemas.NewTableUpdate) -> schemas.NewTableInDB:
        return self.repository.update(item_id, item)

    def delete_item(self, item_id: int) -> bool:
        return self.repository.delete(item_id)
```

5. **Crear Router en `app/api/routers/new_table.py`**:
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.domain import schemas
from app.services.new_table_service import NewTableService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=schemas.NewTableInDB)
def create_item(
    item: schemas.NewTableCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("required.permission"))
):
    service = NewTableService(db)
    return service.create_item(item)

@router.get("/", response_model=List[schemas.NewTableInDB])
def get_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    service = NewTableService(db)
    return service.get_items(skip, limit)

# ... otros endpoints (GET /{id}, PUT, DELETE)
```

6. **Registrar el Router en __init__.py**:
```python
from .new_table import router as new_table_router

__all__ = [..., "new_table_router"]
```

7. **Incluir el Router en main.py**:
```python
from app.api.routers import new_table_router

app.include_router(
    new_table_router,
    prefix="/api/v1/new-table",
    tags=["NewTable"]
)
```

Esta estructura mantiene:
- Separación de responsabilidades
- Patrón Repository para abstracción de datos
- Capa de servicio para lógica de negocio
- DTOs/Schemas para validación y transformación de datos
- Rutas API con dependencias para autenticación/autorización

Recuerda también:
- Agregar tests unitarios
- Documentar los endpoints
- Manejar errores adecuadamente
- Implementar validaciones de negocio en la capa de servicio