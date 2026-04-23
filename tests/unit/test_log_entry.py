# tests/unit/test_log_entry.py
"""LogEntry 数据模型测试"""
import pytest
from datetime import datetime
from backend.models.log_entry import LogEntry


def test_create_log_entry_minimal():
    """测试创建最小化日志条目"""
    log = LogEntry(
        content="Test log content",
        exception_type="NullPointerException",
        severity="HIGH"
    )
    assert log.id is not None
    assert log.content == "Test log content"
    assert log.exception_type == "NullPointerException"
    assert log.severity == "HIGH"
    assert log.created_at is not None


def test_create_log_entry_full():
    """测试创建完整日志条目"""
    log = LogEntry(
        content="Test log",
        exception_type="TimeoutError",
        severity="CRITICAL",
        occurred_at=datetime(2026, 4, 23, 10, 0),
        service_name="user-service",
        stack_trace="at com.example.Service.method(Service.java:42)",
        user_id="user-123"
    )
    assert log.service_name == "user-service"
    assert log.stack_trace is not None
    assert log.user_id == "user-123"


def test_log_entry_to_dict():
    """测试 to_dict 方法"""
    log = LogEntry(
        content="Test",
        exception_type="Other",
        severity="LOW"
    )
    data = log.to_dict()
    assert data["id"] == log.id
    assert data["content"] == "Test"
    assert data["severity"] == "LOW"
    assert "created_at" in data


def test_log_entry_from_dict():
    """测试 from_dict 方法"""
    data = {
        "id": "test-id",
        "content": "Test content",
        "exception_type": "DatabaseError",
        "severity": "MEDIUM",
        "service_name": "order-service"
    }
    log = LogEntry.from_dict(data)
    assert log.id == "test-id"
    assert log.content == "Test content"
    assert log.service_name == "order-service"
