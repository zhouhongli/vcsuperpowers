# backend/routes/logs.py
"""日志管理路由"""
from fastapi import APIRouter, HTTPException
from typing import Optional
from datetime import datetime

from backend.schemas.log_schemas import (
    LogCreate,
    LogResponse,
    LogListResponse,
    BatchDeleteRequest,
)
from backend.main import repository

router = APIRouter()


@router.post("/logs", response_model=LogResponse, status_code=201)
def create_log(log_data: LogCreate):
    """创建日志条目"""
    data = log_data.model_dump()
    data["exception_type"] = data["exception_type"].value
    data["severity"] = data["severity"].value
    if data.get("occurred_at"):
        data["occurred_at"] = data["occurred_at"].isoformat()

    created = repository.create(data)
    return LogResponse(**created)


@router.get("/logs", response_model=LogListResponse)
def get_logs(
    page: int = 1,
    page_size: int = 10,
    exception_type: Optional[str] = None,
    severity: Optional[str] = None,
    service_name: Optional[str] = None,
    search: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
):
    """获取日志列表"""
    result = repository.get_all(
        page=page,
        page_size=page_size,
        exception_type=exception_type,
        severity=severity,
        service_name=service_name,
        search=search,
        date_from=date_from,
        date_to=date_to,
    )
    return LogListResponse(**result)


@router.get("/logs/{log_id}", response_model=LogResponse)
def get_log(log_id: str):
    """获取单条日志详情"""
    log = repository.get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail=f"Log with ID '{log_id}' not found")
    return LogResponse(**log)


@router.put("/logs/{log_id}", response_model=LogResponse)
def update_log(log_id: str, log_data: dict):
    """更新日志"""
    existing = repository.get(log_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Log with ID '{log_id}' not found")

    update_data = {k: v for k, v in log_data.items() if v is not None}
    if "exception_type" in update_data:
        update_data["exception_type"] = str(update_data["exception_type"])
    if "severity" in update_data:
        update_data["severity"] = str(update_data["severity"])

    updated = repository.update(log_id, update_data)
    return LogResponse(**updated)


@router.delete("/logs/{log_id}", status_code=204)
def delete_log(log_id: str):
    """删除单条日志"""
    if not repository.delete(log_id):
        raise HTTPException(status_code=404, detail=f"Log with ID '{log_id}' not found")
    return None


@router.delete("/logs", status_code=204)
def delete_logs_batch(request: BatchDeleteRequest):
    """批量删除日志"""
    repository.delete_batch(request.ids)
    return None
