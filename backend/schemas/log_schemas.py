# backend/schemas/log_schemas.py
"""Pydantic 请求/响应模型"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class ExceptionTypeEnum(str, Enum):
    """异常类型"""
    NULL_POINTER = "NullPointerException"
    TIMEOUT = "TimeoutError"
    DATABASE = "DatabaseError"
    AUTHENTICATION = "AuthenticationError"
    OTHER = "Other"


class SeverityEnum(str, Enum):
    """严重程度"""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class LogCreate(BaseModel):
    """创建日志请求体"""
    content: str = Field(..., min_length=1, description="日志内容")
    exception_type: ExceptionTypeEnum = Field(..., description="异常类型")
    severity: SeverityEnum = Field(..., description="严重程度")
    occurred_at: Optional[datetime] = Field(None, description="发生时间")
    service_name: Optional[str] = Field(None, description="服务名称")
    stack_trace: Optional[str] = Field(None, description="堆栈跟踪")
    user_id: Optional[str] = Field(None, description="用户 ID")


class LogUpdate(BaseModel):
    """更新日志请求体"""
    content: Optional[str] = Field(None, min_length=1, description="日志内容")
    exception_type: Optional[ExceptionTypeEnum] = Field(None, description="异常类型")
    severity: Optional[SeverityEnum] = Field(None, description="严重程度")
    occurred_at: Optional[datetime] = Field(None, description="发生时间")
    service_name: Optional[str] = Field(None, description="服务名称")
    stack_trace: Optional[str] = Field(None, description="堆栈跟踪")
    user_id: Optional[str] = Field(None, description="用户 ID")


class LogResponse(BaseModel):
    """日志响应体"""
    id: str
    content: str
    exception_type: str
    severity: str
    occurred_at: Optional[datetime]
    service_name: Optional[str]
    stack_trace: Optional[str]
    user_id: Optional[str]
    created_at: datetime
    updated_at: datetime


class LogListResponse(BaseModel):
    """日志列表响应体"""
    items: List[LogResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class BatchDeleteRequest(BaseModel):
    """批量删除请求体"""
    ids: List[str]
