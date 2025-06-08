# Performance Metrics Schemas
from enum import Enum
from decimal import Decimal
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class MetricCategoryEnum(str, Enum):
    CLINICAL = "Clinical"
    FINANCIAL = "Financial" 
    OPERATIONAL = "Operational"
    PATIENT_SATISFACTION = "Patient Satisfaction"

class PerformanceMetricBase(BaseModel):
    clinic_id: int
    metric_name: str
    metric_value: Decimal = Field(..., decimal_places=2)
    metric_target: Optional[Decimal] = Field(None, decimal_places=2)
    measurement_date: datetime
    metric_category: MetricCategoryEnum
    description: Optional[str] = None
    notes: Optional[str] = None

class PerformanceMetricCreate(PerformanceMetricBase):
    pass

class PerformanceMetricUpdate(BaseModel):
    metric_name: Optional[str] = None
    metric_value: Optional[Decimal] = Field(None, decimal_places=2)
    metric_target: Optional[Decimal] = Field(None, decimal_places=2)
    measurement_date: Optional[datetime] = None
    metric_category: Optional[MetricCategoryEnum] = None
    description: Optional[str] = None
    notes: Optional[str] = None

class PerformanceMetricInDB(PerformanceMetricBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by_user_id: Optional[int] = None
    updated_by_user_id: Optional[int] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PerformanceMetricResponse(PerformanceMetricInDB):
    clinic: Optional[Dict[str, Any]] = None
    created_by_user: Optional[Dict[str, Any]] = None
    updated_by_user: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
