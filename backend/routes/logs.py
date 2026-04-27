# backend/routes/logs.py
"""日志管理路由"""
from fastapi import APIRouter, HTTPException, Request, UploadFile
from typing import Optional
from datetime import datetime

from backend.schemas.log_schemas import (
    LogResponse,
    LogListResponse,
    BatchDeleteRequest,
)
from backend.main import repository

router = APIRouter()

ALLOWED_FILE_TYPES = {".log", ".txt"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def _check_file_extension(filename: Optional[str]) -> bool:
    """检查文件扩展名是否合法"""
    if not filename:
        return False
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in ALLOWED_FILE_TYPES


@router.post("/logs", response_model=LogResponse, status_code=201)
async def create_log(request: Request):
    """创建日志条目（支持 JSON 和 multipart/form-data 两种格式）"""
    content_type = request.headers.get("content-type", "")

    log_data = None

    if "multipart" in content_type:
        # --- Multipart/form-data 模式（文件上传）---
        form = await request.form()
        file: Optional[UploadFile] = form.get("file")
        text_content = form.get("content")
        exception_type = form.get("exception_type")
        severity = form.get("severity")
        service_name = form.get("service_name") or None
        stack_trace = form.get("stack_trace") or None
        user_id = form.get("user_id") or None
        occurred_at_raw = form.get("occurred_at")

        # 处理文件上传
        file_content = None
        if file and file.filename:
            if not _check_file_extension(file.filename):
                raise HTTPException(
                    status_code=400,
                    detail=f"不支持的文件类型。仅支持 {', '.join(ALLOWED_FILE_TYPES)}"
                )
            raw = await file.read()
            if len(raw) > MAX_FILE_SIZE:
                raise HTTPException(status_code=413, detail="文件大小超过 5MB 限制")
            try:
                file_content = raw.decode("utf-8")
            except UnicodeDecodeError:
                raise HTTPException(status_code=400, detail="文件编码无效，请使用 UTF-8 编码")

        # 文件内容优先于文本内容
        final_content = file_content or text_content
        if not final_content:
            raise HTTPException(status_code=400, detail="必须提供日志内容或上传文件")

        log_data = {
            "content": final_content,
            "exception_type": exception_type,
            "severity": severity,
            "service_name": service_name,
            "stack_trace": stack_trace,
            "user_id": user_id,
        }
        if occurred_at_raw:
            log_data["occurred_at"] = occurred_at_raw

    else:
        # --- JSON 模式（向后兼容）---
        try:
            body = await request.json()
        except Exception:
            raise HTTPException(status_code=400, detail="请求体格式错误")

        log_data = {
            "content": body.get("content"),
            "exception_type": body.get("exception_type"),
            "severity": body.get("severity"),
            "service_name": body.get("service_name"),
            "stack_trace": body.get("stack_trace"),
            "user_id": body.get("user_id"),
        }
        if body.get("occurred_at"):
            log_data["occurred_at"] = body["occurred_at"]

    if not log_data.get("content"):
        raise HTTPException(status_code=400, detail="必须提供日志内容")

    created = repository.create(log_data)
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
