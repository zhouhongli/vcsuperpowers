# backend/models/log_entry.py
"""日志条目数据模型"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class LogEntry:
    """日志条目"""
    content: str
    exception_type: str
    severity: str

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    occurred_at: Optional[datetime] = None
    service_name: Optional[str] = None
    stack_trace: Optional[str] = None
    user_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "id": self.id,
            "content": self.content,
            "exception_type": self.exception_type,
            "severity": self.severity,
            "occurred_at": self.occurred_at.isoformat() if self.occurred_at else None,
            "service_name": self.service_name,
            "stack_trace": self.stack_trace,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "LogEntry":
        """从字典创建"""
        return cls(
            id=data.get("id", str(uuid.uuid4())),
            content=data["content"],
            exception_type=data["exception_type"],
            severity=data["severity"],
            occurred_at=datetime.fromisoformat(data["occurred_at"]) if data.get("occurred_at") else None,
            service_name=data.get("service_name"),
            stack_trace=data.get("stack_trace"),
            user_id=data.get("user_id"),
            created_at=datetime.fromisoformat(data["created_at"]) if data.get("created_at") else datetime.now(),
            updated_at=datetime.fromisoformat(data["updated_at"]) if data.get("updated_at") else datetime.now(),
        )
