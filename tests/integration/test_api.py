# tests/integration/test_api.py
"""API 集成测试"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_repository():
    """每个测试前清空仓库"""
    from backend.main import repository
    repository.clear()
    yield


def test_root():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    assert "智能日志分析与诊断平台" in response.json()["message"]


def test_health():
    """测试健康检查"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_log():
    """测试创建日志"""
    response = client.post("/api/logs", json={
        "content": "Test log content",
        "exception_type": "NullPointerException",
        "severity": "HIGH"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["content"] == "Test log content"
    assert data["id"] is not None


def test_get_logs():
    """测试获取日志列表"""
    client.post("/api/logs", json={"content": "Log 1", "exception_type": "Other", "severity": "LOW"})
    client.post("/api/logs", json={"content": "Log 2", "exception_type": "TimeoutError", "severity": "HIGH"})

    response = client.get("/api/logs")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2


def test_get_log_detail():
    """测试获取日志详情"""
    create_response = client.post("/api/logs", json={
        "content": "Detail test",
        "exception_type": "Other",
        "severity": "MEDIUM"
    })
    log_id = create_response.json()["id"]

    response = client.get(f"/api/logs/{log_id}")
    assert response.status_code == 200
    assert response.json()["content"] == "Detail test"


def test_delete_log():
    """测试删除日志"""
    create_response = client.post("/api/logs", json={
        "content": "To delete",
        "exception_type": "Other",
        "severity": "LOW"
    })
    log_id = create_response.json()["id"]

    response = client.delete(f"/api/logs/{log_id}")
    assert response.status_code == 204


def test_diagnose_log():
    """测试诊断日志"""
    create_response = client.post("/api/logs", json={
        "content": "Null pointer at getInstance()",
        "exception_type": "NullPointerException",
        "severity": "HIGH",
        "stack_trace": "at Service.getInstance(Service.java:42)"
    })
    log_id = create_response.json()["id"]

    response = client.post(f"/api/logs/{log_id}/diagnose")
    assert response.status_code == 200
    data = response.json()
    assert "root_cause" in data
    assert "solution" in data


def test_dashboard_stats():
    """测试仪表盘统计"""
    client.post("/api/logs", json={
        "content": "Log 1",
        "exception_type": "NullPointerException",
        "severity": "HIGH",
        "service_name": "user-service"
    })

    response = client.get("/api/dashboard/stats")
    assert response.status_code == 200
    data = response.json()
    assert "exception_type_distribution" in data
    assert "severity_distribution" in data
    assert "top_services" in data
