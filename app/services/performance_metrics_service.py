from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.data.repositories.performance_metrics_repository import PerformanceMetricsRepository
from app.domain.models.performance_metrics_schemas import (
    PerformanceMetricCreate,
    PerformanceMetricUpdate,
    PerformanceMetricInDB,
    MetricCategoryEnum
)

class PerformanceMetricsService:
    def __init__(self, db: Session):
        self.repository = PerformanceMetricsRepository(db)

    def create_metric(self, metric: PerformanceMetricCreate, created_by_user_id: int) -> PerformanceMetricInDB:
        return self.repository.create(metric, created_by_user_id)

    def get_metric(self, metric_id: int) -> PerformanceMetricInDB:
        metric = self.repository.get_by_id(metric_id)
        if not metric:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Performance metric not found"
            )
        return metric

    def get_metrics(self, skip: int = 0, limit: int = 100) -> List[PerformanceMetricInDB]:
        return self.repository.get_all(skip, limit)

    def get_clinic_metrics(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[PerformanceMetricInDB]:
        return self.repository.get_by_clinic(clinic_id, skip, limit)

    def get_metrics_by_category(self, category: MetricCategoryEnum, skip: int = 0, limit: int = 100) -> List[PerformanceMetricInDB]:
        return self.repository.get_by_category(category, skip, limit)

    def update_metric(
        self, 
        metric_id: int, 
        metric: PerformanceMetricUpdate, 
        updated_by_user_id: int
    ) -> PerformanceMetricInDB:
        updated_metric = self.repository.update(metric_id, metric, updated_by_user_id)
        if not updated_metric:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Performance metric not found"
            )
        return updated_metric

    def delete_metric(self, metric_id: int) -> bool:
        if not self.repository.soft_delete(metric_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Performance metric not found"
            )
        return True
