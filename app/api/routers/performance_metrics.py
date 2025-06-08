from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.domain.schemas import (
    PerformanceMetricCreate,
    PerformanceMetricUpdate,
    PerformanceMetricResponse,
    MetricCategoryEnum
)
from app.services.performance_metrics_service import PerformanceMetricsService
from app.api.dependencies import get_current_user, require_permission

router = APIRouter()

@router.post("/", response_model=PerformanceMetricResponse)
def create_performance_metric(
    metric: PerformanceMetricCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("performance_metrics.crear"))
):
    """
    Crear una nueva métrica de rendimiento.
    """
    service = PerformanceMetricsService(db)
    return service.create_metric(metric, current_user.id)

@router.get("/{metric_id}", response_model=PerformanceMetricResponse)
def get_performance_metric(
    metric_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("performance_metrics.ver"))
):
    """
    Obtener una métrica de rendimiento específica por ID.
    """
    service = PerformanceMetricsService(db)
    return service.get_metric(metric_id)

@router.get("/", response_model=List[PerformanceMetricResponse])
def get_performance_metrics(
    skip: int = 0,
    limit: int = 100,
    clinic_id: Optional[int] = Query(None),
    category: Optional[MetricCategoryEnum] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("performance_metrics.ver"))
):
    """
    Obtener lista de métricas de rendimiento.
    Se puede filtrar por clínica y/o categoría.
    """
    service = PerformanceMetricsService(db)
    
    if clinic_id:
        return service.get_clinic_metrics(clinic_id, skip, limit)
    elif category:
        return service.get_metrics_by_category(category, skip, limit)
    return service.get_metrics(skip, limit)

@router.put("/{metric_id}", response_model=PerformanceMetricResponse)
def update_performance_metric(
    metric_id: int,
    metric: PerformanceMetricUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("performance_metrics.editar"))
):
    """
    Actualizar una métrica de rendimiento existente.
    """
    service = PerformanceMetricsService(db)
    return service.update_metric(metric_id, metric, current_user.id)

@router.delete("/{metric_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_performance_metric(
    metric_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_permission("performance_metrics.eliminar"))
):
    """
    Eliminar una métrica de rendimiento (soft delete).
    """
    service = PerformanceMetricsService(db)
    service.delete_metric(metric_id)
    return {"status": "success"}
