# backend/schemas/diagnosis_schemas.py
"""诊断相关 Pydantic 模型"""
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class DiagnosisResponse(BaseModel):
    """诊断结果响应体"""
    id: str
    log_id: str
    root_cause: str
    solution: str
    severity_assessment: str
    similar_logs: List[str]
    created_at: datetime


class DiagnosisCreateRequest(BaseModel):
    """创建诊断请求体（用于大模型降级）"""
    content: str
    exception_type: str
    severity: str
    service_name: Optional[str] = None
    stack_trace: Optional[str] = None
