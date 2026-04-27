"""文件上传集成测试"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app
import io

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_repository():
    """每个测试前清空仓库"""
    from backend.main import repository
    repository.clear()
    yield


def test_upload_log_file_creates_entry():
    """上传 .log 文件应创建日志条目"""
    file_content = b"java.lang.NullPointerException: Cannot invoke method on null object reference"

    response = client.post(
        "/api/logs",
        data={
            "exception_type": "NullPointerException",
            "severity": "HIGH",
            "service_name": "user-service",
        },
        files={
            "file": ("error.log", io.BytesIO(file_content), "text/plain"),
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert "NullPointerException" in data["content"]
    assert data["exception_type"] == "NullPointerException"
    assert data["severity"] == "HIGH"


def test_upload_log_with_text_and_file_prefers_file():
    """同时提供文本和文件时，文件内容优先"""
    file_content = b"This is from the uploaded file\nwith multiple lines"

    response = client.post(
        "/api/logs",
        data={
            "content": "This is text content",
            "exception_type": "TimeoutError",
            "severity": "MEDIUM",
        },
        files={
            "file": ("debug.log", io.BytesIO(file_content), "text/plain"),
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "This is from the uploaded file\nwith multiple lines"


def test_upload_unsupported_file_type_rejected():
    """上传非 .log/.txt 文件应返回 400"""
    response = client.post(
        "/api/logs",
        data={
            "exception_type": "Other",
            "severity": "LOW",
        },
        files={
            "file": ("report.pdf", b"fake pdf content", "application/pdf"),
        },
    )
    assert response.status_code == 400


def test_post_json_still_works():
    """JSON 提交方式应保持向后兼容"""
    response = client.post(
        "/api/logs",
        json={
            "content": "Test log content via JSON",
            "exception_type": "TimeoutError",
            "severity": "LOW",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "Test log content via JSON"
    assert data["exception_type"] == "TimeoutError"


def test_upload_file_too_large_rejected():
    """上传超过 5MB 的文件应返回 413"""
    large_content = b"x" * (5 * 1024 * 1024 + 1)
    response = client.post(
        "/api/logs",
        data={
            "exception_type": "Other",
            "severity": "LOW",
        },
        files={
            "file": ("huge.log", io.BytesIO(large_content), "text/plain"),
        },
    )
    assert response.status_code == 413
