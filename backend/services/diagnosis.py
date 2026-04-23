# backend/services/diagnosis.py
"""诊断服务"""
from typing import Dict, Any, Optional, List


class DiagnosisService:
    """诊断服务"""

    def __init__(self, repository):
        self.repository = repository
        self._diagnoses: Dict[str, Dict[str, Any]] = {}

    def diagnose(self, log_id: str) -> Dict[str, Any]:
        """诊断日志（占位实现）"""
        log = self.repository.get(log_id)
        if not log:
            raise ValueError(f"Log '{log_id}' not found")

        return {
            "id": "diag-1",
            "log_id": log_id,
            "root_cause": "待实现",
            "solution": "待实现",
            "severity_assessment": log["severity"],
            "similar_logs": [],
            "created_at": "2026-04-23T00:00:00",
        }

    def get_diagnosis(self, log_id: str) -> Optional[Dict[str, Any]]:
        """获取诊断结果"""
        return self._diagnoses.get(log_id)

    def has_diagnosis(self, log_id: str) -> bool:
        """检查是否已有诊断"""
        return log_id in self._diagnoses
