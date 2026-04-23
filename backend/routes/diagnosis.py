# backend/routes/diagnosis.py
"""诊断路由"""
from fastapi import APIRouter, HTTPException

from backend.schemas.diagnosis_schemas import DiagnosisResponse
from backend.main import repository, diagnosis_service

router = APIRouter()


@router.post("/logs/{log_id}/diagnose", response_model=DiagnosisResponse)
def create_diagnosis(log_id: str):
    """创建/获取诊断结果"""
    log = repository.get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail=f"Log with ID '{log_id}' not found")

    try:
        result = diagnosis_service.diagnose(log_id)
        return DiagnosisResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/logs/{log_id}/diagnosis", response_model=DiagnosisResponse)
def get_diagnosis(log_id: str):
    """获取诊断结果"""
    log = repository.get(log_id)
    if not log:
        raise HTTPException(status_code=404, detail=f"Log with ID '{log_id}' not found")

    result = diagnosis_service.get_diagnosis(log_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"No diagnosis found for log '{log_id}'")

    return DiagnosisResponse(**result)
