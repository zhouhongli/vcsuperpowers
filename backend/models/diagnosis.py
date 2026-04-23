# backend/models/diagnosis.py
"""诊断结果数据模型"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import uuid


@dataclass
class Diagnosis:
    """诊断结果"""
    log_id: str
    root_cause: str
    solution: str
    severity_assessment: str

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    similar_logs: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "log_id": self.log_id,
            "root_cause": self.root_cause,
            "solution": self.solution,
            "severity_assessment": self.severity_assessment,
            "similar_logs": self.similar_logs,
            "created_at": self.created_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Diagnosis":
        """从字典创建"""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            log_id=data["log_id"],
            root_cause=data["root_cause"],
            solution=data["solution"],
            severity_assessment=data["severity_assessment"],
            similar_logs=data.get("similar_logs", []),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.now(),
        )
