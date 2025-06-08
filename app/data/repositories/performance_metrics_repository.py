from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime

from app.domain.models.performance_metrics import PerformanceMetrics
from app.domain.models.performance_metrics_schemas import PerformanceMetricCreate, PerformanceMetricUpdate

class PerformanceMetricsRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, metric: PerformanceMetricCreate, created_by_user_id: int) -> PerformanceMetrics:
        db_metric = PerformanceMetrics(
            **metric.model_dump(),
            created_by_user_id=created_by_user_id,
            updated_by_user_id=created_by_user_id
        )
        self.db.add(db_metric)
        self.db.commit()
        self.db.refresh(db_metric)
        return db_metric

    def get_by_id(self, metric_id: int) -> Optional[PerformanceMetrics]:
        return self.db.query(PerformanceMetrics).filter(
            PerformanceMetrics.id == metric_id,
            PerformanceMetrics.deleted_at == None
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[PerformanceMetrics]:
        return self.db.query(PerformanceMetrics)\
            .filter(PerformanceMetrics.deleted_at == None)\
            .offset(skip)\
            .limit(limit)\
            .all()

    def get_by_clinic(self, clinic_id: int, skip: int = 0, limit: int = 100) -> List[PerformanceMetrics]:
        return self.db.query(PerformanceMetrics)\
            .filter(
                PerformanceMetrics.clinic_id == clinic_id,
                PerformanceMetrics.deleted_at == None
            )\
            .offset(skip)\
            .limit(limit)\
            .all()

    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[PerformanceMetrics]:
        return self.db.query(PerformanceMetrics)\
            .filter(
                PerformanceMetrics.metric_category == category,
                PerformanceMetrics.deleted_at == None
            )\
            .offset(skip)\
            .limit(limit)\
            .all()

    def update(self, metric_id: int, metric: PerformanceMetricUpdate, updated_by_user_id: int) -> Optional[PerformanceMetrics]:
        db_metric = self.get_by_id(metric_id)
        if db_metric:
            update_data = metric.model_dump(exclude_unset=True)
            update_data["updated_by_user_id"] = updated_by_user_id
            for field, value in update_data.items():
                setattr(db_metric, field, value)
            self.db.commit()
            self.db.refresh(db_metric)
        return db_metric

    def soft_delete(self, metric_id: int) -> bool:
        db_metric = self.get_by_id(metric_id)
        if db_metric:
            db_metric.deleted_at = datetime.now()
            self.db.commit()
            return True
        return False
